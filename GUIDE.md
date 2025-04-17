# NexusChat Quickstart Guide (for Everyone!)

Welcome to NexusChat! This guide will walk you through installing and using the app—no coding skills needed.

1) Download & Install
---------------------
- Visit www.nexuschat.com and click **Download for macOS**.  
- Open the downloaded **NexusChat-0.4.pkg** file and follow the installer steps.  
- Once finished, you’ll see NexusChat in your Applications.

2) First Launch
---------------
- Open **NexusChat** (from Launchpad or Finder).  
- A browser window will pop up with a simple form:
- **Hugging Face API Token**: Copy your token from https://huggingface.co/settings/tokens and paste it here.  
- **Data Directory**: (Optional) Choose where to store models & chat history. Defaults to `~/Library/Application Support/NexusChat`.  
- **Select Model**: Type or choose a model name (e.g., `mistralAI/mistral-7b-instruct`) from the suggestions.  
- Click **Install & Continue**.

3) Model Download
------------------
- The app will download the model files to your computer.  
- This may take several minutes (model sizes can be GBs).
- Once done, you’ll automatically move to the chat interface.

4) Chatting
-----------
- In your browser, you’ll see a retro ASCII chat window.  
- Type in the box and hit **Send**.  
- The AI will reply offline—in seconds.

5) Changing Models
-------------------
- To install a new model, delete the folder `~/Library/Application Support/NexusChat/models/<model_name>`, then relaunch the app.  
- The installer form will reappear.

Tips & Troubleshooting
----------------------
- If you see errors during download, check your internet connection and Hugging Face token.  
- Models require disk space: ensure you have enough (5–10 GB).  
- For advanced setups (GPU support), install appropriate drivers before running.

Enjoy your private, offline AI assistant!  