import requests
import logging
from typing import Optional, List, Dict
from config import LLAMA_SERVER_URL, REQUEST_TIMEOUT

class AIConnector:

    def __init__(self, server_url: str = LLAMA_SERVER_URL):
        self.server_url = server_url.rstrip('/')
        self.timeout = REQUEST_TIMEOUT
    
    def check_server_health(self) -> bool:
        try:
            response = requests.get(f"{self.server_url}/health", timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    async def get_response(self, messages: List[Dict[str, str]]) -> Optional[str]:
        logging.info(f"Sending request to AI server with {len(messages)} messages.")
        payload = {
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.7,
            "stop": ["<|im_end|>"]
        }
        try:
            response = requests.post(
                f"{self.server_url}/v1/chat/completions",
                json=payload,
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                logging.info(f"Received successful response from AI server.")
                return content
            else:
                logging.error(f"AI server returned an error. Status: {response.status_code}, Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error when requesting AI server: {e}", exc_info=True)
            return None


async def test_llama_connection():
    client = AIConnector()
    if client.check_server_health():
        print("✅ LLaMA server is available")
        # Example messages for testing
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! How are you?"}
        ]
        response = await client.get_response(messages)
        if response:
            print(f"🤖 Response: {response}")
        else:
            print("❌ Failed to get a response")
    else:
        print("❌ LLaMA server is not available")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_llama_connection()) 