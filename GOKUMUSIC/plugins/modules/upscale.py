import os
import aiofiles
import aiohttp
import logging
from config import DEEP_API, BOT_USERNAME
from GOKUMUSIC import app
from pyrogram import Client, filters
from pyrogram.types import Message
from uuid import uuid4

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def image_loader(image: str, link: str) -> str:
    """Download image from a URL and save it locally."""
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            if resp.status == 200:
                async with aiofiles.open(image, mode="wb") as f:
                    await f.write(await resp.read())
                return image
            else:
                logger.error(f"Failed to download image, status code: {resp.status}")
                raise Exception(f"Failed to download image, status code: {resp.status}")

async def upscale_image_api(image_path: str) -> dict:
    """Call the DeepAI API to upscale the image."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.deepai.org/api/torch-srgan",
            data={'image': open(image_path, 'rb')},
            headers={'api-key': DEEP_API}
        ) as resp:
            if resp.status != 200:
                logger.error(f"API request failed with status code: {resp.status}")
                raise Exception(f"API request failed with status code: {resp.status}")
            return await resp.json()

@app.on_message(filters.command("upscale", prefixes="/"))
async def upscale_image(client: Client, message: Message):
    """Handle /upscale command to upscale an image using DeepAI API."""
    chat_id = message.chat.id
    replied = message.reply_to_message

    if not DEEP_API:
        return await message.reply_text("API key is not configured. Cannot upscale the image.")
    
    if not replied or not replied.photo:
        return await message.reply_text("Please reply to an image to upscale it.")
    
    aux = await message.reply_text("Processing the image, please wait...")
    
    image = await replied.download()
    
    try:
        data = await upscale_image_api(image)
        
        if "output_url" not in data:
            logger.error(f"Failed to upscale the image. API response: {data}")
            raise Exception("Failed to upscale the image. API response: " + str(data))
        
        image_link = data["output_url"]
        downloaded_image = await image_loader(image, image_link)
        
        await aux.delete()
        await message.reply_document(downloaded_image)
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await aux.edit_text(f"An error occurred: {e}")
    finally:
        os.remove(image)

