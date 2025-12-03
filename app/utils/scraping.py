import feedparser
import asyncio
from app.claude_api import claude

class TrendScanner:
    # --- Тренды ---
    async def get_reddit_trends(self, subreddit="3Dmodeling"):
        url = f"https://www.reddit.com/r/{subreddit}/top/.rss?t=day"
        feed = feedparser.parse(url)
        posts = []
        for entry in feed.entries[:3]:
            posts.append(f"- {entry.title} (Link: {entry.link})")
        return "\n".join(posts) if posts else "Нет данных RSS."

    async def get_ai_synthetic_trends(self):
        system = "Ты эксперт по трендам в 3D и дизайне."
        prompt = "Какие сейчас тренды в 3D (Blender, Motion Design, NFT)? Дай Топ-5 тем."
        return await claude.generate_response(system, prompt)
    
    # --- Конкуренты ---
    async def analyze_competitor_simulation(self, target: str):
        system = "Ты SMM-аналитик."
        prompt = f"Проанализируй профиль 3D-художника '{target}'. Дай советы по контенту."
        return await claude.generate_response(system, prompt)

    # --- Фриланс (NEW) ---
    async def get_freelance_jobs(self):
        """Парсит Reddit r/forhire + AI симуляция, если пусто"""
        url = "https://www.reddit.com/r/forhire/new/.rss" # Реальный источник
        feed = feedparser.parse(url)
        
        jobs = []
        # Фильтруем по ключевым словам
        keywords = ['3d', 'blender', 'modeler', 'animator', 'motion', 'c4d']
        
        for entry in feed.entries:
            if any(k in entry.title.lower() for k in keywords):
                jobs.append(f"💰 {entry.title}\n🔗 {entry.link}")
        
        if jobs:
            return "🔥 **Найдены свежие заказы:**\n\n" + "\n\n".join(jobs[:5])
        else:
            # Fallback: симуляция, чтобы показать функционал пользователю
            system = "Ты эмулятор биржи фриланса."
            prompt = (
                "Сгенерируй список из 3-х реалистичных (но выдуманных) заказов для 3D-художника "
                "с ценами и описанием задач. Укажи, что это примеры (DEMO)."
            )
            return await claude.generate_response(system, prompt)

scanner = TrendScanner()
