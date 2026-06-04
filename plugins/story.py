import os
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import PREFIXES, OWNER_ID

def is_owner(_, __, m: Message):
    return OWNER_ID == 0 or (m.from_user and m.from_user.id == OWNER_ID)

@Client.on_message(filters.command("story", PREFIXES) & filters.me & filters.create(is_owner))
async def post_story(client: Client, message: Message):
    """
    .story <caption> - reply to photo/video
    Post a Telegram story
    """
    reply = message.reply_to_message
    if not reply or not (reply.photo or reply.video):
        return await message.edit_text("Reply to a photo or video with .story <caption>")
    
    caption = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else ""
    await message.edit_text("📤 Uploading story...")
    
    try:
        media_path = await client.download_media(reply, file_name="story_temp/")
        
        # Default privacy: PUBLIC. Change to enums.StoriesPrivacyRules.CONTACTS if needed
        story = await client.send_story(
            chat_id="me",
            media=media_path,
            caption=caption,
            privacy=enums.StoriesPrivacyRules.PUBLIC,
        )
        
        await message.edit_text(f"✅ Story posted! ID: {story.id}")
        
        # cleanup
        try: os.remove(media_path)
        except: pass
    except Exception as e:
        await message.edit_text(f"❌ Failed to post story: {e}")