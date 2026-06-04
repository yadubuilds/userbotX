import asyncio
import logging
from pyrogram import Client, idle
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import API_ID, API_HASH, SESSION_NAME, PREFIXES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log = logging.getLogger("userbot")

# Global scheduler for scheduled broadcasts
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.start()

app = Client(
    name=SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="plugins"),
    workdir=".",
)

# Make scheduler accessible from plugins
app.scheduler = scheduler

async def main():
    log.info("Starting Userbot...")
    await app.start()
    me = await app.get_me()
    log.info(f"Logged in as {me.first_name} (@{me.username}) [{me.id}]")
    await idle()
    await app.stop()
    log.info("Userbot stopped.")

if __name__ == "__main__":
    asyncio.run(main())