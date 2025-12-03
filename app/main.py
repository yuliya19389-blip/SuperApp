import asyncio
import logging
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from app.config import BOT_TOKEN, WEBHOOK_URL
from app.handlers import base, trends, copywriter, competitors, vision, freelance, planning
from app.utils.scheduler import scheduler_manager

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

# Регистрация всех роутеров
dp.include_router(base.router)
dp.include_router(trends.router)
dp.include_router(copywriter.router)
dp.include_router(competitors.router)
dp.include_router(vision.router)     # Vision
dp.include_router(freelance.router)  # Jobs
dp.include_router(planning.router)   # Calendar

@app.on_event("startup")
async def on_startup():
    scheduler_manager.start(bot)
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)

@app.post("/")
async def webhook(req: dict): return {"status": "ok"}
@app.get("/")
async def health(): return {"status": "running"}

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
