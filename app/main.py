#!/usr/bin/env python3
"""
NexusChat main application server.
"""
import os
import json
import threading
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, jsonify
from huggingface_hub import login
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import uuid
import shutil
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Application directories
APP_NAME = "NexusChat"
# Default directory for config (always store config here)
DEFAULT_DATA_DIR = Path.home() / "Library" / "Application Support" / APP_NAME
CONFIG_PATH = DEFAULT_DATA_DIR / "config.json"

def get_data_dir() -> Path:
    # returns user-specified data directory or default
    if CONFIG_PATH.exists():
        cfg = load_config()
        return Path(cfg.get('data_dir', str(DEFAULT_DATA_DIR)))
    return DEFAULT_DATA_DIR

def get_models_dir() -> Path:
    return get_data_dir() / "models"

def get_chroma_dir() -> Path:
    return get_data_dir() / "chromadb"

app = Flask(__name__, template_folder="templates")
app.secret_key = 'change-this-to-a-random-secret'

def slug(model_name: str) -> str:
    return model_name.replace('/', '_')

def ensure_dirs():
    # ensure default config dir
    DEFAULT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    # ensure data directories for models and memory
    data_dir = get_data_dir()
    (data_dir / "models").mkdir(parents=True, exist_ok=True)
    (data_dir / "chromadb").mkdir(parents=True, exist_ok=True)

def load_config() -> dict:
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(cfg: dict):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(cfg, f)

def download_model(model_name: str):
    """Download and save model and tokenizer locally."""
    target = get_models_dir() / slug(model_name)
    if target.exists():
        return
    # download
    tok = AutoTokenizer.from_pretrained(model_name)
    mdl = AutoModelForCausalLM.from_pretrained(model_name)
    target.mkdir(parents=True, exist_ok=True)
    mdl.save_pretrained(target)
    tok.save_pretrained(target)

_pipeline = None
def get_pipeline():
    global _pipeline
    if _pipeline is None:
        cfg = load_config()
        model_name = cfg.get('model')
        path = get_models_dir() / slug(model_name)
        tok = AutoTokenizer.from_pretrained(path)
        mdl = AutoModelForCausalLM.from_pretrained(path)
        _pipeline = pipeline('text-generation', model=mdl, tokenizer=tok)
    return _pipeline

@app.route('/', methods=['GET', 'POST'])
def index():
    ensure_dirs()
    if not CONFIG_PATH.exists():
        if request.method == 'POST':
            token = request.form.get('token')
            model_name = request.form.get('model')
            data_dir = request.form.get('data_dir')
            # login and save config
            login(token)
            save_config({'token': token, 'model': model_name, 'data_dir': data_dir})
            # start download in background
            threading.Thread(target=download_model, args=(model_name,), daemon=True).start()
            return redirect(url_for('installing'))
        # show form
        # default list of suggested models (user may type custom)
        models = [
            'mistralAI/mistral-7b-instruct',
            'meta-llama/Llama-2-7b-chat-hf',
            'gpt2'
        ]
        # default data directory
        default = str(DEFAULT_DATA_DIR)
        return render_template('index.html', models=models, default_data_dir=default)
    return redirect(url_for('chat'))

@app.route('/installing')
def installing():
    if CONFIG_PATH.exists():
        cfg = load_config()
        if (get_models_dir() / slug(cfg.get('model'))).exists():
            return redirect(url_for('chat'))
    return render_template('installing.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

def init_memory():
    """Initialize vector store and embedding model for chat memory."""
    global chroma_client, chroma_collection, embedder
    data_dir = get_data_dir()
    db_dir = get_chroma_dir()
    chroma_client = chromadb.Client(Settings(chroma_db_impl="sqlite", persist_directory=str(db_dir)))
    chroma_collection = chroma_client.get_or_create_collection(name="chat_memory")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return chroma_client, chroma_collection, embedder

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json() or {}
    prompt = data.get('prompt', '')
    # initialize memory and embeddings
    client, collection, embed = init_memory()
    # encode and retrieve similar past messages
    q_vec = embed.encode(prompt).tolist()
    results = collection.query(query_embeddings=[q_vec], n_results=5, include=['documents'])
    contexts = results.get('documents', [[]])[0]
    # build prompt with memory context
    if contexts:
        memory_str = '\n'.join(contexts)
        full_prompt = f"Memory:\n{memory_str}\nUser: {prompt}\nAssistant:"
    else:
        full_prompt = f"User: {prompt}\nAssistant:"
    # generate response
    pipe = get_pipeline()
    res = pipe(full_prompt, max_new_tokens=150, do_sample=True, top_p=0.9)
    text = res[0].get('generated_text', '')
    # extract assistant reply
    answer = text.split('Assistant:')[-1].strip()
    # store user and assistant messages in memory
    collection.add(documents=[prompt], embeddings=[q_vec], ids=[str(uuid.uuid4())], metadatas=[{'role': 'user'}])
    a_vec = embed.encode(answer).tolist()
    collection.add(documents=[answer], embeddings=[a_vec], ids=[str(uuid.uuid4())], metadatas=[{'role': 'assistant'}])
    client.persist()
    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
  
@app.route('/api/reset', methods=['POST'])
def api_reset():
    """Reset chat history (vector store)"""
    # remove persistent memory directory
    data_dir = get_data_dir()
    db_dir = get_chroma_dir()
    if db_dir.exists():
        shutil.rmtree(db_dir)
    return jsonify({'status': 'reset'})