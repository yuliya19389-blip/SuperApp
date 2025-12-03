from aiogram import Router, F
from aiogram.types import Message
from app.gemini_api import gemini

router = Router()

@router.message(F.photo)
async def handle_vision(message: Message):
    await message.answer("👀 Вижу рендер! Включаю режим Арт-директора... (Gemini Vision)")
    
    # 1. Получаем файл
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path
    
    # 2. Скачиваем байты
    binary_io = await message.bot.download_file(file_path)
    image_bytes = binary_io.read()
    
    # 3. Отправляем в API (байты напрямую)
    prompt = (
        "Ты профессиональный 3D Lead Artist. Проведи ревью этой работы.\n"
        "1. Композиция и кадрирование.\n"
        "2. Свет и цвет.\n"
        "3. Технические детали.\n"
        "4. Оценка (1-10) и совет."
    )
    
    response = await gemini.analyze_image(image_bytes, prompt)
    await message.answer(response)
