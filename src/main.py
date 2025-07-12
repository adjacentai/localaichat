import asyncio
import logging
from aiogram import Bot, Dispatcher

from .assistant.ai_connector import AIConnector
from .assistant.dialog_history import DialogHistory
from config import BOT_TOKEN
from .handlers import register_handlers


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    bot = Bot(token=BOT_TOKEN)
except ValueError:
    logging.critical("Error: Invalid token format. Please check BOT_TOKEN in your config.")
    exit()

dp = Dispatcher()
ai_connector = AIConnector()
dialog_history = DialogHistory()

processing_users = set()

register_handlers(dp, bot, ai_connector, dialog_history, processing_users)


async def main():
    logging.info("Starting bot...")

    if not ai_connector.check_server_health():
        logging.warning("LLaMA server is not available. The bot may not work correctly.")
    else:
        logging.info("LLaMA server is available.")

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
    except Exception as e:
        logging.critical(f"Critical error on bot startup: {e}", exc_info=True) 