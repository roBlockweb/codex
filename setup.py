from setuptools import setup

APP = ['app/main.py']
DATA_FILES = ['app/templates/index.html', 'app/templates/installing.html', 'app/templates/chat.html']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['flask', 'transformers', 'huggingface_hub', 'requests', 'chromadb', 'sentence_transformers'],
    'includes': ['flask', 'transformers', 'huggingface_hub', 'requests', 'chromadb', 'sentence_transformers'],
    'plist': {
        'CFBundleName': 'NexusChat',
        'CFBundleShortVersionString': '0.3',
        'CFBundleIdentifier': 'com.roblock.nexuschat'
    }
}

setup(
    app=APP,
    name='NexusChat',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)