import base64
from aiogram import Router, F
from aiogram.types import Message
from app.claude_api import claude

router = Router()

@router.message(F.photo)
async def handle_vision(message: Message):
    await message.answer("👀 Вижу рендер! Включаю режим Арт-директора... (Анализ займет 5-10 сек)")
    
    # 1. Скачиваем фото (берем лучшее качество)
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    
    # Скачиваем в память
    binary_io = await message.bot.download_file(file_path)
    
    # 2. Кодируем в base64 для Claude
    base64_image = base64.b64encode(binary_io.read()).decode("utf-8")
    
    # 3. Отправляем в API
    prompt = (
        "Ты профессиональный 3D Lead Artist. Проведи ревью этой работы.\n"
        "1. Композиция и кадрирование.\n"
        "2. Свет и цвет (Lighting & Color).\n"
        "3. Технические детали (текстуры, моделинг).\n"
        "4. Общая оценка (1-10) и главный совет по улучшению."
    )
    
    response = await claude.analyze_image(base64_image, prompt)
    await message.answer(response)
