import anthropic
import base64
import json
from app.config import CLAUDE_API_KEY

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=CLAUDE_API_KEY)
        self.model = "claude-3-5-sonnet-latest"

    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Обычный текстовый ответ"""
        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Ошибка Claude API: {e}"

    async def analyze_image(self, base64_image: str, prompt: str) -> str:
        """Анализ изображений (Vision)"""
        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image,
                                },
                            },
                            {"type": "text", "text": prompt}
                        ],
                    }
                ],
            )
            return message.content[0].text
        except Exception as e:
            return f"Ошибка Vision API: {e}"

    async def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        """Генерация чистого JSON (для календаря)"""
        full_prompt = user_prompt + "\nВерни ТОЛЬКО валидный JSON без Markdown форматирования."
        text = await self.generate_response(system_prompt, full_prompt)
        # Очистка от возможных ```json ... ```
        clean_text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(clean_text)
        except:
            return {} # Возврат пустого dict при ошибке парсинга

claude = ClaudeClient()
