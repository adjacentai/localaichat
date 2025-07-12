import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Telegram Bot ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the .env file.")

# --- AI Model & Server ---
MODEL_PATH = os.getenv("MODEL_PATH")
if not MODEL_PATH:
    raise ValueError("MODEL_PATH is not set in the .env file.")

# Extract model name from the path for display purposes
MODEL_NAME = Path(MODEL_PATH).name

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("LLAMA_PORT", "8000"))
LLAMA_SERVER_URL = f"http://{HOST}:{PORT}"

# --- Dialog Context ---
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "300"))
MAX_CONTEXT_MESSAGES = int(os.getenv("MAX_CONTEXT_MESSAGES", "20")) 