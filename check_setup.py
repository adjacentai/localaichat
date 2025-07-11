#!/usr/bin/env python3
"""
Тестирование компонентов Telegram бота
"""

import asyncio
from config_example import BOT_TOKEN, LLAMA_SERVER_URL
# 🐍 Изучаем: Импорты из пакета `src`
# Теперь, когда наш код в пакете, мы импортируем его вот так.
from src.llama_client import LlamaClient
from src.context_manager import ContextManager


async def main():
    print("🧪 Запуск тестирования Telegram бота с LLaMA")
    print("="*50)
    
    # --- Тест 1: Конфигурация ---
    print("\n1️⃣  Тестирование конфигурации...")
    config_ok = True
    if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
        print("❌ BOT_TOKEN не настроен в config_example.py!")
        config_ok = False
    else:
        print("✅ BOT_TOKEN настроен.")
    
    if not LLAMA_SERVER_URL:
        print("❌ LLAMA_SERVER_URL не настроен в config_example.py!")
        config_ok = False
    else:
        print(f"✅ LLAMA_SERVER_URL: {LLAMA_SERVER_URL}")

    # --- Тест 2: Менеджер контекста ---
    print("\n2️⃣  Тестирование ContextManager...")
    context_ok = True
    try:
        cm = ContextManager()
        cm.add_message(1, "user", "test")
        if cm.get_context_info(1)["messages"] != 1:
            raise ValueError("Message count is incorrect")
        cm.clear_context(1)
        if cm.get_context_info(1)["messages"] != 0:
            raise ValueError("Context clearing failed")
        print("✅ ContextManager работает корректно.")
    except Exception as e:
        print(f"❌ Ошибка в ContextManager: {e}")
        context_ok = False
        
    # --- Тест 3: LLaMA Клиент ---
    print("\n3️⃣  Тестирование LlamaClient...")
    llama_ok = True
    try:
        client = LlamaClient()
        # Проверяем не асинхронный метод `check_server_health`
        is_healthy = client.check_server_health()
        if is_healthy:
            print("✅ LLaMA сервер доступен по эндпоинту /health.")
            # Теперь проверяем асинхронный метод
            # response = await client.send_message("Это тестовый запрос, отвечать не нужно.")
            # print(f"✅ Тестовый запрос к /completion прошел. Ответ: {'OK' if response else 'Нет ответа'}")
        else:
            print("⚠️ LLaMA сервер недоступен. Убедитесь, что он запущен.")
            # Этот тест не будем считать провальным, т.к. сервер может быть выключен
    except Exception as e:
        print(f"❌ Ошибка в LlamaClient: {e}")
        llama_ok = False
        
    # --- Результаты ---
    print("\n" + "="*50)
    if all([config_ok, context_ok, llama_ok]):
        print("🎉 ВСЕ ОСНОВНЫЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("🚀 Можно запускать бота командой: python -m src.bot")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ. Исправьте ошибки.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"💥 Критическая ошибка при тестировании: {e}") 