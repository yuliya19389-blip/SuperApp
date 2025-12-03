from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from app.gemini_api import gemini
from ics import Calendar, Event
import io

router = Router()

@router.message(F.text == "📅 Создать план")
async def create_plan(message: Message):
    await message.answer("🧠 Gemini думает над стратегией...")
    
    system = "Ты SMM-стратег для 3D-художников."
    # Для Gemini JSON Mode нужно четко описать схему в промпте
    user_prompt = (
        "Создай контент-план на 5 дней. "
        "Верни список JSON объектов. Используй такую схему: "
        "[{'date': 'YYYY-MM-DD', 'title': 'Theme', 'description': 'Details'}]"
    )
    
    data = await gemini.generate_json(system, user_prompt)
    
    if not data:
        await message.answer("Ошибка генерации. Попробуй еще раз.")
        return

    text_report = "📅 **Твой контент-план:**\n\n"
    cal = Calendar()
    
    for item in data:
        date_str = item.get('date', 'N/A')
        title = item.get('title', 'Post')
        desc = item.get('description', '')
        
        text_report += f"🔹 **{date_str}**: {title}\n_{desc}_\n\n"
        
        try:
            e = Event()
            e.name = f"Post: {title}"
            e.begin = f"{date_str} 10:00:00"
            e.description = desc
            cal.events.add(e)
        except:
            pass

    await message.answer(text_report, parse_mode="Markdown")
    
    ics_data = cal.serialize()
    file_bytes = io.BytesIO(ics_data.encode('utf-8'))
    input_file = BufferedInputFile(file_bytes.getvalue(), filename="content_plan.ics")
    
    await message.answer_document(document=input_file, caption="📂 Файл для календаря")
