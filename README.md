# NexusChat v0.4

An offline, open-source AI chat application for macOS with a retro CLI vibe.  
Built by roBlock & OpenAI Codex.  

Features:
- One-click installer (.pkg) for macOS
- Automatic environment & dependency setup via py2app
- Supports Hugging Face models (e.g., Mistral 7B, LLaMA 3)
- Local model download & offline inference
- Simple ASCII UI served in your browser

Getting Started
-------------
1. Download `NexusChat-0.4.pkg` from Releases.  
2. Run the installer; it will place NexusChat in `/Applications`.  
3. Launch **NexusChat** from Launchpad or the Applications folder.  

First Run
---------
On first launch, NexusChat will open a browser window to:
1. Enter your Hugging Face API token.  
2. Select a compatible model for your machine.  
3. Click **Install** to download the model locally.  

Once installed, the chat interface loads automatically.  
Type your messages and get AI-powered responses—all offline.

Packaging from Source
---------------------
```bash
git clone https://github.com/roBlockweb/codex.git
cd codex
brew install python3 pkgbuild  # if not already installed
pip install -r requirements.txt
bash build_pkg.sh
```

License
-------
MIT License (see LICENSE file, if included)

## How It Works

- Configuration: On first run, enter your Hugging Face token, select a model, and choose where to store data.  
- Config (`config.json`) is saved to `~/Library/Application Support/NexusChat`.  
- Model Management: Downloads model weights & tokenizer into `data_dir/models/{model}`.  
- Memory Store: Uses ChromaDB (SQLite) in `data_dir/chromadb` with SentenceTransformer embeddings to store and retrieve past messages as vector memories.  
- Chat API: A Flask server hosts `/api/chat`, which integrates memory context and uses local Transformers for generation.  
- Persistence & Reset: Conversation history persists locally and can be cleared via the **Reset History** button.

## Releasing v0.4

1. Tag the release:
   ```bash
   git tag -a v0.4 -m "Release v0.4"
   git push --tags
   ```
2. Build the installer:
   ```bash
   bash build_pkg.sh
   ```
3. Upload `NexusChat-0.4.pkg` to your website (e.g., `www.nexuschat.com/downloads/`).
4. Draft a GitHub Release (v0.4) and attach the installer.
5. Announce your commercial release!