import requests
import json
from typing import Optional
from config_example import LLAMA_SERVER_URL, REQUEST_TIMEOUT


class LlamaClient:
    """
    Клиент для работы с LLaMA сервером
    """
    
    def __init__(self, server_url: str = LLAMA_SERVER_URL):
        """
        Инициализация клиента
        """
        self.server_url = server_url.rstrip('/')
        self.timeout = REQUEST_TIMEOUT
    
    async def send_message(self, message: str, context: Optional[str] = None) -> Optional[str]:
        """
        Отправляет сообщение в LLaMA и получает ответ
        """
        try:
            if context:
                full_prompt = f"{context}\nUser: {message}\nAssistant:"
            else:
                full_prompt = f"User: {message}\nAssistant:"
            
            payload = {
                "prompt": full_prompt,
                "max_tokens": 512,
                "temperature": 0.7,
                "stop": ["User:", "\n\n"]
            }
            
            print(f"🚀 Отправляем запрос к LLaMA: {self.server_url}/completion")
            
            response = requests.post(
                f"{self.server_url}/completion",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("content", "").strip()
                print(f"✅ Получен ответ от LLaMA: {answer[:50]}...")
                return answer
            else:
                print(f"❌ Ошибка LLaMA сервера: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            print("❌ Не удается подключиться к LLaMA серверу. Убедитесь, что он запущен.")
            return None
        except requests.exceptions.Timeout:
            print("⏰ Таймаут запроса к LLaMA серверу. Сервер может быть перегружен.")
            return None
        except Exception as e:
            print(f"❌ Неожиданная ошибка при запросе к LLaMA: {e}")
            return None

    def check_server_health(self) -> bool:
        """
        Проверяет доступность LLaMA сервера
        """
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


async def test_llama_connection():
    """
    Тестирует подключение к LLaMA серверу
    """
    client = LlamaClient()
    
    if client.check_server_health():
        print("✅ LLaMA сервер доступен")
        response = await client.send_message("Привет! Как дела?")
        if response:
            print(f"🤖 Ответ: {response}")
        else:
            print("❌ Не удалось получить ответ")
    else:
        print("❌ LLaMA сервер недоступен")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_llama_connection()) 