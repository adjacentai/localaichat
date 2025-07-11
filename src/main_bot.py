import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# 🐍 Изучаем: Относительные импорты внутри пакета
# Точка (.) означает "из этой же папки" (из src)
from .llama_client import LlamaClient
from .context_manager import ContextManager

# А этот импорт работает, т.к. мы запускаем из корня `LocalAiChat`
from config_example import BOT_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Инициализация объектов ---
# 🐍 Изучаем: Глобальные объекты
# Эти объекты создаются один раз при запуске и используются во всем приложении.
# Это эффективно, т.к. мы не создаем новые подключения и менеджеры при каждом сообщении.
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
llama_client = LlamaClient()
context_manager = ContextManager()


# --- Клавиатуры ---
def get_reset_keyboard() -> InlineKeyboardMarkup:
    """Создает и возвращает inline-клавиатуру."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Сбросить контекст", callback_data="reset_context")]
    ])
    return keyboard


# --- Обработчики команд и callback'ов ---
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start."""
    user_id = message.from_user.id
    context_manager.clear_context(user_id)
    await message.answer(
        "🔄 Диалог сброшен!\n\n"
        "👋 Привет! Я бот на базе LLaMA модели. Просто напиши мне.",
        reply_markup=get_reset_keyboard()
    )
    logging.info(f"User {user_id} started the bot and cleared context.")


@dp.callback_query(lambda c: c.data == 'reset_context')
async def callback_reset_context(callback: CallbackQuery):
    """Обработчик нажатия на кнопку сброса контекста."""
    user_id = callback.from_user.id
    context_manager.clear_context(user_id)
    await callback.answer("🔄 Контекст сброшен!")
    await callback.message.edit_text(
        "🔄 Контекст диалога сброшен!\n\nМожете начать новый разговор.",
        reply_markup=get_reset_keyboard()
    )
    logging.info(f"User {user_id} cleared context via button.")


# --- Основной обработчик сообщений ---
@dp.message()
async def chat_handler(message: Message) -> None:
    """Основной обработчик для диалога с LLaMA."""
    user_id = message.from_user.id
    user_text = message.text
    
    # Игнорируем пустые сообщения
    if not user_text:
        return

    logging.info(f"Received message from {user_id}: '{user_text}'")

    try:
        # Показываем, что бот "печатает"
        await bot.send_chat_action(user_id, 'typing')

        # Добавляем сообщение пользователя в историю
        context_manager.add_message(user_id, "user", user_text)
        current_context = context_manager.get_context(user_id)

        # Отправляем запрос к LLaMA
        llama_response = await llama_client.send_message(user_text, current_context)

        if llama_response:
            context_manager.add_message(user_id, "assistant", llama_response)
            context_info = context_manager.get_context_info(user_id)
            response_with_info = (
                f"{llama_response}\n\n"
                f"💾 Контекст: {context_info['messages']}/{context_info['max_messages']}"
            )
            await message.answer(response_with_info, reply_markup=get_reset_keyboard())
        else:
            await message.answer(
                "😔 Извините, не могу сейчас ответить. Проблема на стороне ИИ-модели. "
                "Попробуйте позже.",
                reply_markup=get_reset_keyboard()
            )

    except Exception as e:
        logging.error(f"Error processing message for user {user_id}: {e}", exc_info=True)
        await message.answer(
            "😔 Произошла внутренняя ошибка. Попробуйте сбросить диалог.",
            reply_markup=get_reset_keyboard()
        )


# --- Точка входа ---
async def main() -> None:
    """Главная функция для запуска бота."""
    logging.info("Starting bot...")

    if not await llama_client.check_server_health():
        logging.warning("LLaMA server is not available. The bot may not function correctly.")
    else:
        logging.info("LLaMA server is available.")

    # Запуск long-polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
    except Exception as e:
        logging.critical(f"Bot failed to start: {e}", exc_info=True) 