from typing import List, Dict
# 🐍 Изучаем: Относительный импорт
# Поскольку config_example.py находится вне пакета src, 
# а запускать мы будем из корня проекта, Python найдет его.
# Команда запуска: python -m src.bot
from config_example import MAX_CONTEXT_MESSAGES


class ContextManager:
    """
    Менеджер контекста для хранения истории сообщений
    """
    
    def __init__(self):
        """
        Инициализация менеджера контекста
        """
        self.user_contexts: Dict[int, List[str]] = {}
        self.max_messages = MAX_CONTEXT_MESSAGES
    
    def add_message(self, user_id: int, role: str, message: str) -> None:
        """
        Добавляет сообщение в контекст пользователя
        """
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = []
            print(f"🆕 Создан новый контекст для пользователя {user_id}")
        
        formatted_message = f"{role.capitalize()}: {message}"
        self.user_contexts[user_id].append(formatted_message)
        
        if len(self.user_contexts[user_id]) > self.max_messages:
            removed = self.user_contexts[user_id].pop(0)
            print(f"📝 Удалено старое сообщение: {removed[:30]}...")
        
        print(f"💾 Контекст пользователя {user_id}: {len(self.user_contexts[user_id])} сообщений")
    
    def get_context(self, user_id: int) -> str:
        """
        Получает контекст пользователя как строку
        """
        if user_id not in self.user_contexts:
            return ""
        
        context = "\n".join(self.user_contexts[user_id])
        return context
    
    def clear_context(self, user_id: int) -> None:
        """
        Очищает контекст пользователя
        """
        if user_id in self.user_contexts:
            message_count = len(self.user_contexts[user_id])
            del self.user_contexts[user_id]
            print(f"🗑️ Очищен контекст пользователя {user_id} ({message_count} сообщений)")
        else:
            print(f"⚠️ Контекст пользователя {user_id} уже пуст")
    
    def get_context_info(self, user_id: int) -> Dict[str, int]:
        """
        Получает информацию о контексте пользователя
        """
        if user_id not in self.user_contexts:
            return {"messages": 0, "max_messages": self.max_messages}
        
        return {
            "messages": len(self.user_contexts[user_id]),
            "max_messages": self.max_messages
        }
    
    def get_all_users(self) -> List[int]:
        """
        Получает список всех пользователей с контекстом
        """
        return list(self.user_contexts.keys())


def demo_context_manager():
    """
    Демонстрация работы менеджера контекста
    """
    print("🧪 Демонстрация ContextManager")
    cm = ContextManager()
    user_id = 123
    
    cm.add_message(user_id, "user", "Привет!")
    cm.add_message(user_id, "assistant", "Привет! Как дела?")
    cm.add_message(user_id, "user", "Отлично! А у тебя?")
    
    context = cm.get_context(user_id)
    print(f"\n📜 Контекст:\n{context}")
    
    info = cm.get_context_info(user_id)
    print(f"\n📊 Информация: {info}")
    
    cm.clear_context(user_id)
    print(f"\n📊 После очистки: {cm.get_context_info(user_id)}")


if __name__ == "__main__":
    demo_context_manager() 