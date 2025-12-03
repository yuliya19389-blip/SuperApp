import google.generativeai as genai
import PIL.Image
import io
import json
from app.config import GEMINI_API_KEY

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        # Используем Flash для скорости и бесплатного тира
        self.model_name = "gemini-1.5-flash" 
        self.model = genai.GenerativeModel(self.model_name)

    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Обычный текстовый ответ"""
        try:
            # В Gemini system prompt передается при создании модели или через инструкцию
            model = genai.GenerativeModel(
                self.model_name,
                system_instruction=system_prompt
            )
            response = await model.generate_content_async(user_prompt)
            return response.text
        except Exception as e:
            return f"Ошибка Gemini API: {e}"

    async def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        """Анализ изображений (Vision)"""
        try:
            # Gemini любит Pillow Image
            img = PIL.Image.open(io.BytesIO(image_bytes))
            
            model = genai.GenerativeModel(self.model_name)
            # Передаем промпт и картинку списком
            response = await model.generate_content_async([prompt, img])
            return response.text
        except Exception as e:
            return f"Ошибка Vision API: {e}"

    async def generate_json(self, system_prompt: str, user_prompt: str) -> list:
        """Генерация чистого JSON (Native JSON Mode)"""
        try:
            model = genai.GenerativeModel(
                self.model_name,
                system_instruction=system_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            response = await model.generate_content_async(user_prompt)
            # Gemini вернет строку JSON, парсим её
            return json.loads(response.text)
        except Exception as e:
            print(f"JSON Error: {e}")
            return []

# Глобальный инстанс
gemini = GeminiClient()
