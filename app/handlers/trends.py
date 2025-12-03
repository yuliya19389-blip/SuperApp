from aiogram import Router, F, types
from aiogram.filters import Command
from app.utils.scraping import scanner
from app.claude_api import claude

router = Router()

@router.message(F.text == "🔍 Тренды")
@router.message(Command("trends"))
async def cmd_trends(message: types.Message):
    await message.answer("🔍 Собираю данные о трендах...")
    reddit = await scanner.get_reddit_trends("blender")
    ai_trends = await scanner.get_ai_synthetic_trends()
    
    system = "Ты редактор новостей CG."
    prompt = f"Данные Reddit:\n{reddit}\nGlobal AI:\n{ai_trends}\nСоставь отчет Топ-5 трендов для 3D артиста."
    
    res = await claude.generate_response(system, prompt)
    await message.answer(res)
