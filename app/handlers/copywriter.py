from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.claude_api import claude

router = Router()
class CopyState(StatesGroup):
    waiting = State()

@router.message(F.text == "✍️ Копирайтер")
async def start_copy(message: types.Message, state: FSMContext):
    await message.answer("Пришли текст/идею поста:")
    await state.set_state(CopyState.waiting)

@router.message(CopyState.waiting)
async def process_copy(message: types.Message, state: FSMContext):
    res = await claude.generate_response("Ты SMM-копирайтер.", f"Улучши текст для соцсетей: {message.text}")
    await message.answer(res)
    await state.clear()
