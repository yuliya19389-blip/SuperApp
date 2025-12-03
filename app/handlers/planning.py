from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from app.claude_api import claude
from ics import Calendar, Event
from datetime import datetime, timedelta
import io

router = Router()

@router.message(F.text == "📅 Создать план")
async def create_plan(message: Message):
    await message.answer("🧠 Генерирую стратегию контента на неделю...")
    
    # 1. Генерация текста и данных через Claude
    system = "Ты SMM-стратег для 3D-художников."
    user_prompt = (
        "Создай контент-план на ближайшие 5 дней (начиная с завтра). "
        "Верни JSON формат: список объектов с полями 'date' (YYYY-MM-DD), 'title' (тема поста), 'description' (кратко о чем)."
    )
    
    # Получаем JSON
    data = await claude.generate_json(system, user_prompt)
    
    if not data or not isinstance(data, list):
        await message.answer("Ошибка генерации плана. Попробуй еще раз.")
        return

    # 2. Формируем красивый текст для чата
    text_report = "📅 **Твой контент-план:**\n\n"
    cal = Calendar()
    
    for item in data:
        date_str = item.get('date', 'N/A')
        title = item.get('title', 'Post')
        desc = item.get('description', '')
        
        text_report += f"🔹 **{date_str}**: {title}\n_{desc}_\n\n"
        
        # Создаем событие календаря
        try:
            e = Event()
            e.name = f"Post: {title}"
            e.begin = f"{date_str} 10:00:00" # Ставим на 10 утра
            e.description = desc
            cal.events.add(e)
        except:
            pass

    # 3. Отправляем текст
    await message.answer(text_report, parse_mode="Markdown")
    
    # 4. Создаем и отправляем .ics файл
    ics_data = cal.serialize()
    file_bytes = io.BytesIO(ics_data.encode('utf-8'))
    input_file = BufferedInputFile(file_bytes.getvalue(), filename="content_plan.ics")
    
    await message.answer_document(
        document=input_file, 
        caption="📂 Скачай этот файл и открой, чтобы добавить в календарь (Google/Apple)."
    )
