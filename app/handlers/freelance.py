from aiogram import Router, F
from aiogram.types import Message
from app.utils.scraping import scanner

router = Router()

@router.message(F.text == "💸 Искать заказы")
async def search_jobs(message: Message):
    await message.answer("🛰 Сканирую биржи фриланса и сообщества...")
    
    report = await scanner.get_freelance_jobs()
    
    await message.answer(report, parse_mode="Markdown")
