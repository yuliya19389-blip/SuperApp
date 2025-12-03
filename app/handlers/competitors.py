from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from app.utils.scraping import scanner

router = Router()

@router.message(Command("analyze"))
async def analyze(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer("Пиши: /analyze <имя>")
        return
    res = await scanner.analyze_competitor_simulation(command.args)
    await message.answer(res)
