from pyrogram import Client, filters
from pyrogram.types import Message, InputPhoneContact
from config import PREFIXES, OWNER_ID

def is_owner(_, __, m: Message):
    return OWNER_ID == 0 or (m.from_user and m.from_user.id == OWNER_ID)

@Client.on_message(filters.command("savecontact", PREFIXES) & filters.me & filters.create(is_owner))
async def save_contact(client: Client, message: Message):
    """
    .savecontact <phone> <first_name> [last_name]
    Example: .savecontact +919876543210 John Doe
    """
    if len(message.command) < 3:
        return await message.edit_text("Usage: .savecontact <phone> <first_name> [last_name]")
    
    phone = message.command[1]
    first_name = message.command[2]
    last_name = " ".join(message.command[3:]) if len(message.command) > 3 else ""
    
    await message.edit_text("💾 Saving contact...")
    try:
        contact = InputPhoneContact(phone=phone, first_name=first_name, last_name=last_name)
        result = await client.import_contacts([contact])
        if result.users:
            user = result.users[0]
            await message.edit_text(f"✅ Contact saved: {user.first_name} [{user.id}]")
        else:
            await message.edit_text("❌ Failed to save contact")
    except Exception as e:
        await message.edit_text(f"❌ Error: {e}")