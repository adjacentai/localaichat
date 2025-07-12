from typing import List, Dict
from config import MAX_CONTEXT_MESSAGES

class DialogHistory:

    def __init__(self):
        # Now stores tuples of (role, message)
        self.user_contexts: Dict[int, List[tuple[str, str]]] = {}
        self.max_messages = MAX_CONTEXT_MESSAGES
    
    def add_message(self, user_id: int, role: str, message: str) -> None:
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = []
        
        # Store raw role and message
        self.user_contexts[user_id].append((role, message))
        
        # Trim context if it exceeds max size
        if len(self.user_contexts[user_id]) > self.max_messages:
            self.user_contexts[user_id].pop(0)
    
    def get_context(self, user_id: int) -> List[tuple[str, str]]:
        return self.user_contexts.get(user_id, [])
    
    def clear_context(self, user_id: int) -> None:
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            
    def get_context_info(self, user_id: int) -> Dict[str, int]:
        count = len(self.user_contexts.get(user_id, []))
        return {"messages": count, "max_messages": self.max_messages}


def demo_context_manager():
    print("🧪 Demonstrating ContextManager")
    cm = DialogHistory()
    user_id = 123
    
    cm.add_message(user_id, "user", "Hello!")
    cm.add_message(user_id, "assistant", "Hi! How are you?")
    cm.add_message(user_id, "user", "Great! And you?")
    
    context = cm.get_context(user_id)
    print(f"\n📜 Context:\n{context}")
    
    info = cm.get_context_info(user_id)
    print(f"\n📊 Info: {info}")
    
    cm.clear_context(user_id)
    print(f"\n📊 After clearing: {cm.get_context_info(user_id)}")


if __name__ == "__main__":
    demo_context_manager() 