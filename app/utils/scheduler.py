from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from app.claude_api import claude

class SchedulerManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.users = set()

    def add_user(self, chat_id):
        self.users.add(chat_id)

    async def send_daily(self, bot: Bot):
        if not self.users: return
        content = await claude.generate_response("Ты ментор.", "Дай совет дня для 3D художника.")
        for uid in self.users:
            try: await bot.send_message(uid, f"🔔 **Совет дня**\n{content}")
            except: pass

    def start(self, bot: Bot):
        self.scheduler.add_job(self.send_daily, 'cron', hour=10, args=[bot])
        self.scheduler.start()

scheduler_manager = SchedulerManager()
