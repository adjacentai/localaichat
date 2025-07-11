import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Импортируем наши модули
from config_example import BOT_TOKEN
from llama_client import LlamaClient
from context_manager import ContextManager

# 🐍 Изучаем: Импорт новых типов для inline клавиатур

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем объекты
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем экземпляры наших классов
llama_client = LlamaClient()
context_manager = ContextManager()


# 🔘 Функция для создания inline клавиатуры
def get_reset_keyboard() -> InlineKeyboardMarkup:
    """
    Создает inline клавиатуру с кнопкой сброса контекста
    
    🐍 Изучаем:
    - Создание inline кнопок
    - Callback данные
    - Возврат клавиатуры
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔄 Сбросить контекст", 
            callback_data="reset_context"
        )]
    ])
    return keyboard


# 🎯 Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start - сбрасывает диалог
    """
    user_id = message.from_user.id
    
    # Очищаем контекст пользователя
    context_manager.clear_context(user_id)
    
    await message.answer(
        "🔄 Диалог сброшен!\n\n"
        "👋 Привет! Я бот с LLaMA моделью!\n"
        "💬 Просто напиши мне сообщение и я отвечу\n"
        "🔄 Используй /start для сброса диалога\n\n"
        "💾 Я запоминаю последние 20 сообщений для контекста",
        reply_markup=get_reset_keyboard()
    )
    print(f"🟢 Пользователь {user_id} запустил бота")


# 🔘 Обработчик нажатия на inline кнопку
@dp.callback_query()
async def callback_handler(callback: CallbackQuery) -> None:
    """
    Обработчик callback запросов от inline кнопок
    
    🐍 Изучаем:
    - Обработка callback данных
    - Ответ на callback запросы
    - Редактирование сообщений
    """
    user_id = callback.from_user.id
    
    if callback.data == "reset_context":
        # Очищаем контекст
        context_manager.clear_context(user_id)
        
        # Отвечаем на callback (убирает "часики" с кнопки)
        await callback.answer("🔄 Контекст сброшен!")
        
        # Редактируем сообщение
        await callback.message.edit_text(
            "🔄 Контекст диалога сброшен!\n\n"
            "Теперь можете начать новый разговор.",
            reply_markup=get_reset_keyboard()
        )
        
        print(f"🔄 Пользователь {user_id} сбросил контекст через кнопку")


# 📝 Обработчик всех текстовых сообщений
@dp.message()
async def chat_handler(message: Message) -> None:
    """
    Главный обработчик сообщений - с inline кнопкой
    
    🐍 Изучаем:
    - Добавление клавиатуры к ответам
    - Обновленная обработка сообщений
    """
    user_id = message.from_user.id
    user_text = message.text
    
    print(f"📨 Сообщение от {user_id}: {user_text}")
    
    try:
        # Добавляем сообщение пользователя в контекст
        context_manager.add_message(user_id, "user", user_text)
        
        # Получаем текущий контекст
        current_context = context_manager.get_context(user_id)
        
        # Показываем, что бот печатает
        await message.bot.send_chat_action(user_id, "typing")
        
        # Отправляем запрос к LLaMA
        llama_response = await llama_client.send_message(user_text, current_context)
        
        if llama_response:
            # Добавляем ответ бота в контекст
            context_manager.add_message(user_id, "assistant", llama_response)
            
            # Получаем информацию о контексте для отображения
            context_info = context_manager.get_context_info(user_id)
            
            # Добавляем информацию о контексте к ответу
            response_with_info = (
                f"{llama_response}\n\n"
                f"💾 Контекст: {context_info['messages']}/{context_info['max_messages']} сообщений"
            )
            
            # Отправляем ответ с inline кнопкой
            await message.answer(
                response_with_info,
                reply_markup=get_reset_keyboard()
            )
            
            print(f"💾 Контекст: {context_info['messages']}/{context_info['max_messages']}")
            
        else:
            # Если LLaMA недоступен
            await message.answer(
                "😔 Извините, сейчас я не могу ответить.\n"
                "🔧 Проблема с LLaMA сервером.\n\n"
                "Попробуйте позже или проверьте настройки сервера.",
                reply_markup=get_reset_keyboard()
            )
    
    except Exception as e:
        print(f"❌ Ошибка при обработке сообщения: {e}")
        await message.answer(
            "😔 Произошла ошибка при обработке сообщения.\n"
            "Попробуйте еще раз.",
            reply_markup=get_reset_keyboard()
        )


# 🚀 Главная функция запуска бота
async def main() -> None:
    """
    Главная асинхронная функция с проверками
    """
    print("🚀 Бот запускается...")
    
    # Проверяем доступность LLaMA сервера
    if llama_client.check_server_health():
        print("✅ LLaMA сервер доступен")
    else:
        print("⚠️ LLaMA сервер недоступен. Бот будет работать с ошибками.")
    
    print("🤖 Бот готов к работе!")
    print("🔘 Доступна inline кнопка для сброса контекста")
    
    # Запускаем бота
    await dp.start_polling(bot)


# 🎬 Запуск программы
if __name__ == '__main__':
    """
    🐍 Изучаем:
    - Финальная версия бота
    - Все функции интегрированы
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}") 