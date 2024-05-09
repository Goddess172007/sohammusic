
import imghdr
import os
from asyncio import gather
from traceback import format_exc

from pyrogram import filters
from pyrogram.errors import (
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from GOKUMUSIC import app
from config import BOT_USERNAME
from GOKUMUSIC.utils.errors import capture_err

from GOKUMUSIC.utils.files import (
    get_document_from_file_id,
    resize_file_to_sticker_size,
    upload_document,
)

from GOKUMUSIC.utils.stickerset import (
    add_sticker_to_set,
    create_sticker,
    create_sticker_set,
    get_sticker_set_by_name,
)

# -----------

MAX_STICKERS = (
    120  # would be better if we could fetch this limit directly from telegram
)
SUPPORTED_TYPES = ["jpeg", "png", "webp"]
# ------------------------------------------
@app.on_message(filters.command("get_sticker"))
@capture_err
async def sticker_image(_, message: Message):
    r = message.reply_to_message

    if not r:
        return await message.reply("Reply to a sticker.")

    if not r.sticker:
        return await message.reply("Reply to a sticker.")

    m = await message.reply("Sending..")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        *[
            message.reply_photo(f),
            message.reply_document(f),
        ]
    )

    await m.delete()
    os.remove(f)
#----------------
@app.on_message(filters.command("kang"))
@capture_err
async def kang(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a sticker/image to kang it.")
    
    if not message.from_user:
        return await message.reply_text("You are anon admin, kang stickers in my pm.")

    msg = await message.reply_text("Kanging Sticker..")

    # Extract emoji from command arguments or use default emoji
    args = message.text.split()
    sticker_emoji = args[1] if len(args) > 1 else "🤔"

    # Get the sticker or image file from the replied message
    file_id = message.reply_to_message.sticker.file_id
    file_name = "sticker.png"  # default file name

    if message.reply_to_message.document:
        file_id = message.reply_to_message.document.file_id
        file_name = message.reply_to_message.document.file_name
    
    try:
        # Download the file
        file_path = await get_document_from_file_id(file_id)

        # Check if the file is a supported image type
        image_type = imghdr.what(file_path)
        if image_type not in SUPPORTED_TYPES:
            return await msg.edit("Unsupported file format.")

        # Resize the image if necessary
        file_path = await resize_file_to_sticker_size(file_path)

        # Open the file
        with open(file_path, "rb") as file:
            # Create a sticker from the file
            sticker = await create_sticker(file, sticker_emoji)

        # Create or find a sticker set to add the sticker
        pack_name = f"f_{message.from_user.id}_by_{BOT_USERNAME}"
        sticker_set = await get_sticker_set_by_name(client, pack_name)
        if not sticker_set:
            sticker_set = await create_sticker_set(client, message.from_user.id, f"{message.from_user.first_name}'s kang pack", pack_name, [sticker])
        elif sticker_set.set.count >= MAX_STICKERS:
            return await msg.edit("Sticker pack is full.")

        # Add the sticker to the sticker set
        await add_sticker_to_set(client, sticker_set, sticker)

        # Provide feedback to the user
        await msg.edit(f"Sticker kanged to [Pack](t.me/addstickers/{pack_name})\nEmoji: {sticker_emoji}")
    
    except Exception as e:
        error_message = str(e)
        await msg.edit(error_message)
        print(format_exc())
    finally:
        # Clean up the temporary files
        if os.path.exists(file_path):
            os.remove(file_path)
