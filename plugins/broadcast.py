import asyncio
import shlex
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait, RPCError
from config import PREFIXES, DEFAULT_INTERVAL, OWNER_ID

def is_owner(_, __, m: Message):
    return OWNER_ID == 0 or (m.from_user and m.from_user.id == OWNER_ID)

async def send_with_interval(client, user_id, text, media=None, interval=2.0):
    try:
        if media:
            await client.copy_message(user_id, media.chat.id, media.id)
        elif text:
            await client.send_message(user_id, text)
        await asyncio.sleep(interval)
        return True
    except FloodWait as e:
        await asyncio.sleep(e.value + 1)
        return await send_with_interval(client, user_id, text, media, interval)
    except RPCError:
        return False

def parse_args(text):
    """Parse --interval 2 --schedule '2024-12-31 23:59'"""
    args = {"interval": DEFAULT_INTERVAL, "schedule": None, "text": ""}
    if not text:
        return args
    try:
        parts = shlex.split(text)
    except:
        parts = text.split()
    
    remaining = []
    i = 0
    while i < len(parts):
        if parts[i] == "--interval" and i+1 < len(parts):
            args["interval"] = float(parts[i+1]); i+=2
        elif parts[i] == "--schedule" and i+1 < len(parts):
            args["schedule"] = parts[i+1]; i+=2
        else:
            remaining.append(parts[i]); i+=1
    args["text"] = " ".join(remaining)
    return args

@Client.on_message(filters.command(["bcdm", "broadcast_dm"], PREFIXES) & filters.me & filters.create(is_owner))
async def broadcast_dm(client: Client, message: Message):
    """
    .bcdm [--interval 2] [--schedule "2025-12-25 10:00"] <text>
    Reply to a message to broadcast it
    """
    await message.edit_text("🔍 Parsing...")
    
    args = parse_args(message.text.split(maxsplit=1)[1] if len(message.command) > 1 else "")
    text = args["text"]
    interval = args["interval"]
    schedule_time = args["schedule"]
    reply = message.reply_to_message
    
    if not text and not reply:
        return await message.edit_text("Usage: .bcdm [--interval 2] [--schedule 'YYYY-MM-DD HH:MM'] <text> or reply")
    
    # Get all private chats
    await message.edit_text("📥 Collecting DM chats...")
    dialogs = []
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_bot and not dialog.chat.is_deleted:
            dialogs.append(dialog.chat.id)
    
    total = len(dialogs)
    
    async def job():
        sent = 0
        failed = 0
        status = await client.send_message("me", f"🚀 Starting DM broadcast to {total} chats (interval {interval}s)")
        for uid in dialogs:
            ok = await send_with_interval(client, uid, text, reply, interval)
            if ok: sent += 1
            else: failed += 1
        await status.edit(f"✅ DM Broadcast done\nSent: {sent}\nFailed: {failed}")
    
    if schedule_time:
        try:
            run_at = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M")
            client.scheduler.add_job(job, 'date', run_date=run_at)
            await message.edit_text(f"⏰ Scheduled DM broadcast to {total} users at {run_at} (interval {interval}s)")
        except Exception as e:
            await message.edit_text(f"❌ Invalid schedule format. Use YYYY-MM-DD HH:MM\n{e}")
    else:
        await message.edit_text(f"🚀 Broadcasting to {total} DMs...")
        asyncio.create_task(job())

@Client.on_message(filters.command(["bccontacts", "broadcast_contacts"], PREFIXES) & filters.me & filters.create(is_owner))
async def broadcast_contacts(client: Client, message: Message):
    """
    .bccontacts <text> or reply
    Broadcast to all contacts
    """
    args = parse_args(message.text.split(maxsplit=1)[1] if len(message.command) > 1 else "")
    text = args["text"]
    interval = args["interval"]
    reply = message.reply_to_message
    
    if not text and not reply:
        return await message.edit_text("Usage: .bccontacts <text> or reply")
    
    await message.edit_text("📇 Fetching contacts...")
    contacts = await client.get_contacts()
    ids = [u.id for u in contacts if not u.is_bot and not u.is_deleted]
    
    sent = 0
    for uid in ids:
        ok = await send_with_interval(client, uid, text, reply, interval)
        if ok: sent += 1
        if sent % 10 == 0:
            await message.edit_text(f"📤 Sending... {sent}/{len(ids)}")
    
    await message.edit_text(f"✅ Contacts broadcast complete. Sent to {sent}/{len(ids)}")