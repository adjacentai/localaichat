from typing import List, Dict

SYSTEM_PROMPT = """You are a helpful and friendly AI assistant named LocalAI.
You should provide concise and accurate answers.
You are running on a local machine, powered by a Hermes model.
"""

def create_main_prompt(dialog_history: List[tuple[str, str]]) -> List[Dict[str, str]]:
    """
    Creates a prompt in ChatML format for Hermes models.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for role, message in dialog_history:
        messages.append({"role": role, "content": message})
    return messages 