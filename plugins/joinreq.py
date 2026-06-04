import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from config import PREFIXES, DEFAULT_INTERVAL, OWNER_ID

def is_owner(_, __, m: Message):
    return OWNER_ID == 0 or (m.from_user and m.from_user.id == OWNER_ID)

@Client.on_message(filters.command(["reqdm", "joinmsg"], PREFIXES) & filters.me & filters.create(is_owner))
async def message_join_requests(client: Client, message: Message):
    """
    .reqdm <chat_id/username> <message>
    Send DM to all pending join request users in a group/channel
    Also sends the group invite link
    """
    if len(message.command) < 3:
        return await message.edit_text("Usage: .reqdm <chat> <message>\nExample: .reqdm @mygroup Hello, here's the link")
    
    chat = message.command[1]
    text = message.text.split(maxsplit=2)[2]
    
    await message.edit_text(f"📥 Fetching join requests for {chat}...")
    
    try:
        chat_obj = await client.get_chat(chat)
        invite_link = chat_obj.invite_link or (await client.export_chat_invite_link(chat_obj.id))
    except Exception as e:
        return await message.edit_text(f"❌ Can't get chat: {e}")
    
    sent = 0
    failed = 0
    
    async for req in client.get_chat_join_requests(chat_obj.id):
        user = req.user
        try:
            msg = f"{text}\n\n🔗 Join Link: {invite_link}"
            await client.send_message(user.id, msg)
            sent += 1
            await asyncio.sleep(DEFAULT_INTERVAL)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except:
            failed += 1
        
        if (sent + failed) % 5 == 0:
            await message.edit_text(f"📤 Progress: sent {sent}, failed {failed}")
    
    await message.edit_text(f"✅ Done messaging join requests\nSent: {sent}\nFailed: {failed}\nLink: {invite_link}")