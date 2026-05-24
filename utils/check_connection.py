import asyncio
import aiohttp
import sys
from pathlib import Path

# Добавляем родительскую папку в путь, чтобы импортировать config
sys.path.append(str(Path(__file__).parent.parent))
from config import WORKER_URL, BOT_TOKEN

async def check_worker():
    url = f"{WORKER_URL}/bot{BOT_TOKEN}/getMe"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()
                print("Статус:", resp.status)
                print("Ответ:", data)
                if data.get("ok"):
                    print("✅ Proxy is working! Bot:", data["result"]["username"])
                else:
                    print("❌ Error:", data.get("description"))
        except Exception as e:
            print("❌ Couldn't connect:", e)

if __name__ == "__main__":
    asyncio.run(check_worker())