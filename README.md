# 🤖 LLaMA Telegram Bot

Простой и качественный Telegram бот для работы с локальными LLaMA моделями через llama-cpp-python сервер.

## ✨ Возможности

- 💬 **Диалог с LLaMA моделью** - умная беседа с ИИ
- 🧠 **Контекст диалога** - запоминает последние 20 сообщений  
- 🔄 **Сброс контекста** - команда `/start` и inline кнопка
- 🚀 **Асинхронная обработка** - быстрые ответы
- 🛡️ **Обработка ошибок** - стабильная работа
- 🔧 **Простая настройка** - минимум конфигурации

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
git clone <your-repo-url>
cd LocalAiChat
pip install -r requirements.txt
```

### 2. Настройка бота

1. Получите токен бота у [@BotFather](https://t.me/BotFather) в Telegram
2. Обновите `BOT_TOKEN` в файле `config_example.py`:

```python
BOT_TOKEN = "your_actual_bot_token_here"
```

### 3. Запуск LLaMA сервера

Установите llama-cpp-python с серверными возможностями:

```bash
pip install llama-cpp-python[server]
```

Запустите сервер с вашей моделью:

```bash
python -m llama_cpp.server \
  --model path/to/your/model.gguf \
  --host 0.0.0.0 \
  --port 8080
```

### 4. Тестирование

Проверьте все компоненты перед запуском:

```bash
python test_bot.py
```

### 5. Запуск бота

```bash
python bot.py
```

## 📁 Структура проекта

```
LocalAiChat/
├── bot.py              # Основной файл бота
├── llama_client.py     # Клиент для работы с LLaMA API
├── context_manager.py  # Менеджер контекста диалогов
├── config_example.py   # Конфигурация
├── test_bot.py         # Тестирование компонентов
├── requirements.txt    # Зависимости Python
└── README.md          # Документация
```

## ⚙️ Конфигурация

Настройте параметры в `config_example.py`:

| Параметр | Описание | По умолчанию |
|----------|----------|-------------|
| `BOT_TOKEN` | Токен Telegram бота | `"your_bot_token_here"` |
| `LLAMA_SERVER_URL` | URL LLaMA сервера | `"http://localhost:8080"` |
| `MAX_CONTEXT_MESSAGES` | Максимум сообщений в контексте | `20` |
| `REQUEST_TIMEOUT` | Таймаут запросов (сек) | `30` |

## 🎯 Использование

1. **Начало диалога**: Отправьте `/start` боту
2. **Общение**: Просто пишите сообщения боту
3. **Сброс контекста**: Используйте `/start` или нажмите кнопку "🔄 Сбросить контекст"

## 🛠️ Требования

- Python 3.8+
- aiogram 3.3.0+
- requests
- Запущенный llama-cpp-python сервер
- Telegram Bot Token

## 🔧 Диагностика проблем

### Бот не отвечает
- Проверьте правильность `BOT_TOKEN`
- Убедитесь что бот запущен

### Ошибки LLaMA
- Проверьте доступность сервера: `curl http://localhost:8080/health`
- Убедитесь что модель загружена
- Проверьте `LLAMA_SERVER_URL` в конфигурации

### Тестирование
Запустите `python test_bot.py` для диагностики всех компонентов.

## 🤝 Участие в разработке

Мы приветствуем вклад в развитие проекта! 

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

## 🙏 Благодарности

- [aiogram](https://github.com/aiogram/aiogram) - Telegram Bot API framework
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - Python bindings для llama.cpp
- Сообщество разработчиков ИИ

## 📧 Контакты

Если у вас есть вопросы или предложения, создайте [issue](../../issues) в репозитории.

---

⭐ Поставьте звезду, если проект был полезен! 