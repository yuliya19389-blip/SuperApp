from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from app.utils.scheduler import scheduler_manager

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    scheduler_manager.add_user(message.chat.id)
    
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="✍️ Копирайтер"), KeyboardButton(text="💸 Искать заказы")],
        [KeyboardButton(text="📅 Создать план"), KeyboardButton(text="🔍 Тренды")]
    ], resize_keyboard=True)
    
    await message.answer(
        "Привет! Я 3D SMM Assistant.\n\n"
        "**Новые функции:**\n"
        "👁️ **Vision:** Отправь мне картинку рендера — я дам фидбек.\n"
        "💸 **Фриланс:** Поиск заказов.\n"
        "📅 **Планнер:** Составлю контент-план и файл календаря.\n\n"
        "Выбери действие в меню или отправь фото!",
        reply_markup=kb,
        parse_mode="Markdown"
    )
