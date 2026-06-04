import os
import sys
import asyncio
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from config import PREFIXES, REPO_PATH, OWNER_ID

def is_owner(_, __, m: Message):
    return OWNER_ID == 0 or (m.from_user and m.from_user.id == OWNER_ID)

@Client.on_message(filters.command("update", PREFIXES) & filters.me & filters.create(is_owner))
async def update_bot(client: Client, message: Message):
    """Git pull and restart"""
    await message.edit_text("🔄 Pulling updates...")
    try:
        # Run git pull
        proc = await asyncio.create_subprocess_shell(
            "git pull",
            cwd=REPO_PATH,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        output = (stdout + stderr).decode().strip()
        
        if proc.returncode == 0:
            await message.edit_text(f"✅ Update successful:\n<pre>{output}</pre>\n\n♻️ Restarting...")
            await asyncio.sleep(1)
            os.execv(sys.executable, [sys.executable, "main.py"])
        else:
            await message.edit_text(f"❌ Update failed:\n<pre>{output}</pre>")
    except Exception as e:
        await message.edit_text(f"❌ Error: {e}")

@Client.on_message(filters.command("restart", PREFIXES) & filters.me & filters.create(is_owner))
async def restart_bot(client: Client, message: Message):
    await message.edit_text("♻️ Restarting userbot...")
    await asyncio.sleep(1)
    os.execv(sys.executable, [sys.executable, "main.py"])