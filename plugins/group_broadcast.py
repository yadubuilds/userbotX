import asyncio
import shlex
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from config import PREFIXES, DEFAULT_INTERVAL, OWNER_ID

def is_owner(_, __, m: Message):
    return OWNER_ID == 0 or (m.from_user and m.from_user.id == OWNER_ID)

def parse_args(text):
    args = {"interval": DEFAULT_INTERVAL, "schedule": None, "text": ""}
    if not text: return args
    try: parts = shlex.split(text)
    except: parts = text.split()
    remaining = []
    i=0
    while i < len(parts):
        if parts[i]=="--interval" and i+1 < len(parts):
            args["interval"]=float(parts[i+1]); i+=2
        elif parts[i]=="--schedule" and i+1 < len(parts):
            args["schedule"]=parts[i+1]; i+=2
        else:
            remaining.append(parts[i]); i+=1
    args["text"]=" ".join(remaining)
    return args

@Client.on_message(filters.command(["bcgroup", "broadcast_group"], PREFIXES) & filters.me & filters.create(is_owner))
async def broadcast_group_members(client: Client, message: Message):
    """
    .bcgroup <chat_id/username> [--interval 2] [--schedule 'YYYY-MM-DD HH:MM'] <message>
    Reply to message to broadcast it to all group members via DM
    """
    if len(message.command) < 2:
        return await message.edit_text("Usage: .bcgroup <chat> [--interval 2] <text> or reply")
    
    chat = message.command[1]
    raw = message.text.split(maxsplit=2)[2] if len(message.command) > 2 else ""
    args = parse_args(raw)
    text = args["text"]
    interval = args["interval"]
    schedule = args["schedule"]
    reply = message.reply_to_message
    
    if not text and not reply:
        return await message.edit_text("Provide text or reply to a message")
    
    await message.edit_text(f"👥 Fetching members of {chat}...")
    
    try:
        members = []
        async for m in client.get_chat_members(chat):
            if m.user and not m.user.is_bot and not m.user.is_deleted and not m.user.is_self:
                members.append(m.user.id)
    except Exception as e:
        return await message.edit_text(f"❌ Error: {e}")
    
    total = len(members)
    
    async def job():
        sent = 0
        failed = 0
        status = await client.send_message("me", f"🚀 Starting group broadcast to {total} members")
        for uid in members:
            try:
                if reply:
                    await client.copy_message(uid, reply.chat.id, reply.id)
                else:
                    await client.send_message(uid, text)
                sent += 1
                await asyncio.sleep(interval)
            except FloodWait as e:
                await asyncio.sleep(e.value + 2)
            except:
                failed += 1
        await status.edit(f"✅ Group broadcast done\nChat: {chat}\nSent: {sent}/{total}\nFailed: {failed}")
    
    if schedule:
        try:
            run_at = datetime.strptime(schedule, "%Y-%m-%d %H:%M")
            client.scheduler.add_job(job, 'date', run_date=run_at)
            await message.edit_text(f"⏰ Scheduled broadcast to {total} members at {run_at}")
        except Exception as e:
            await message.edit_text(f"❌ Bad schedule: {e}")
    else:
        await message.edit_text(f"🚀 Broadcasting to {total} members (interval {interval}s)...")
        asyncio.create_task(job())