# config.py - Конфигурация нашего Telegram бота
# Скопируйте этот файл в config.py и заполните реальными значениями

# 🤖 Telegram Bot Token (получите у @BotFather в Telegram)
BOT_TOKEN = "your_bot_token_here"

# 🦙 LLaMA Server Configuration  
LLAMA_SERVER_URL = "http://localhost:8080"
LLAMA_MODEL_NAME = "llama-3b"

# ⚙️ Bot Settings
MAX_CONTEXT_MESSAGES = 20  # Максимум сообщений в контексте
REQUEST_TIMEOUT = 30       # Таймаут запроса к LLaMA в секундах 