#!/usr/bin/env python3
"""
Тестирование компонентов Telegram бота

🐍 Изучаем:
- Модульное тестирование
- Проверка конфигурации
- Диагностика проблем
"""

import asyncio
import sys
from config_example import BOT_TOKEN, LLAMA_SERVER_URL, MAX_CONTEXT_MESSAGES
from llama_client import LlamaClient
from context_manager import ContextManager


def test_config():
    """
    Тестирует конфигурацию
    
    🐍 Изучаем:
    - Проверка настроек
    - Валидация данных
    """
    print("🔧 Тестирование конфигурации...")
    
    # Проверяем BOT_TOKEN
    if BOT_TOKEN == "your_bot_token_here":
        print("❌ BOT_TOKEN не настроен!")
        print("   Получите токен у @BotFather и обновите config_example.py")
        return False
    elif len(BOT_TOKEN) < 40:
        print("❌ BOT_TOKEN выглядит некорректно!")
        return False
    else:
        print(f"✅ BOT_TOKEN настроен: {BOT_TOKEN[:10]}...")
    
    # Проверяем URL LLaMA
    print(f"✅ LLaMA Server URL: {LLAMA_SERVER_URL}")
    print(f"✅ Max Context Messages: {MAX_CONTEXT_MESSAGES}")
    
    return True


def test_context_manager():
    """
    Тестирует менеджер контекста
    
    🐍 Изучаем:
    - Тестирование собственных классов
    - Проверка функциональности
    """
    print("\n💾 Тестирование ContextManager...")
    
    try:
        cm = ContextManager()
        test_user_id = 12345
        
        # Тест добавления сообщений
        cm.add_message(test_user_id, "user", "Тестовое сообщение 1")
        cm.add_message(test_user_id, "assistant", "Ответ бота 1")
        cm.add_message(test_user_id, "user", "Тестовое сообщение 2")
        
        # Тест получения контекста
        context = cm.get_context(test_user_id)
        if len(context) > 0:
            print("✅ Добавление и получение сообщений работает")
        else:
            print("❌ Проблема с получением контекста")
            return False
        
        # Тест информации о контексте
        info = cm.get_context_info(test_user_id)
        if info['messages'] == 3:
            print("✅ Подсчет сообщений работает корректно")
        else:
            print(f"❌ Ожидалось 3 сообщения, получено {info['messages']}")
            return False
        
        # Тест очистки контекста
        cm.clear_context(test_user_id)
        cleared_info = cm.get_context_info(test_user_id)
        if cleared_info['messages'] == 0:
            print("✅ Очистка контекста работает")
        else:
            print("❌ Проблема с очисткой контекста")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в ContextManager: {e}")
        return False


async def test_llama_client():
    """
    Тестирует LLaMA клиент
    
    🐍 Изучаем:
    - Асинхронное тестирование
    - Проверка внешних зависимостей
    """
    print("\n🦙 Тестирование LlamaClient...")
    
    try:
        client = LlamaClient()
        
        # Тест проверки здоровья сервера
        is_healthy = client.check_server_health()
        if is_healthy:
            print("✅ LLaMA сервер доступен")
            
            # Тест отправки сообщения
            print("🚀 Тестирование отправки сообщения...")
            response = await client.send_message("Тестовое сообщение для проверки")
            
            if response:
                print(f"✅ Получен ответ: {response[:50]}...")
                return True
            else:
                print("❌ Не удалось получить ответ от LLaMA")
                return False
        else:
            print("⚠️ LLaMA сервер недоступен")
            print("   Убедитесь что llama-cpp-python сервер запущен на", LLAMA_SERVER_URL)
            return False
            
    except Exception as e:
        print(f"❌ Ошибка в LlamaClient: {e}")
        return False


def print_instructions():
    """
    Выводит инструкции по использованию бота
    
    🐍 Изучаем:
    - Документация для пользователя
    - Пошаговые инструкции
    """
    print("\n" + "="*60)
    print("📋 ИНСТРУКЦИИ ПО ЗАПУСКУ БОТА")
    print("="*60)
    
    print("\n1️⃣ Настройте конфигурацию:")
    print("   - Получите токен бота у @BotFather в Telegram")
    print("   - Обновите BOT_TOKEN в config_example.py")
    
    print("\n2️⃣ Запустите LLaMA сервер:")
    print("   pip install llama-cpp-python[server]")
    print("   python -m llama_cpp.server --model path/to/your/model.gguf --host 0.0.0.0 --port 8080")
    
    print("\n3️⃣ Запустите бота:")
    print("   python bot.py")
    
    print("\n4️⃣ Функции бота:")
    print("   ✅ Диалог с LLaMA моделью")
    print("   ✅ Контекст до 20 сообщений")
    print("   ✅ Команда /start для сброса")
    print("   ✅ Inline кнопка 'Сбросить контекст'")
    
    print("\n🐍 Что вы изучили:")
    print("   ✅ Асинхронное программирование (async/await)")
    print("   ✅ Классы и объекты")
    print("   ✅ Работа с API (HTTP запросы)")
    print("   ✅ Telegram Bot API через aiogram")
    print("   ✅ Управление состоянием приложения")
    print("   ✅ Обработка ошибок")
    print("   ✅ Модульность кода")


async def main():
    """
    Главная функция тестирования
    
    🐍 Изучаем:
    - Последовательное тестирование
    - Сбор результатов
    """
    print("🧪 Запуск тестирования Telegram бота с LLaMA")
    print("="*50)
    
    all_tests_passed = True
    
    # Тест конфигурации
    if not test_config():
        all_tests_passed = False
    
    # Тест менеджера контекста
    if not test_context_manager():
        all_tests_passed = False
    
    # Тест LLaMA клиента
    if not await test_llama_client():
        all_tests_passed = False
    
    # Результаты
    print("\n" + "="*50)
    if all_tests_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("🚀 Бот готов к запуску!")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        print("🔧 Исправьте ошибки перед запуском бота")
    
    # Показываем инструкции
    print_instructions()


if __name__ == "__main__":
    asyncio.run(main()) 