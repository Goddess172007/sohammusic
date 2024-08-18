import requests
from pyrogram import filters
from pyrogram.types import InputMediaPhoto
from GOKUMUSIC import app

ANILIST_API_URL = 'https://graphql.anilist.co'

@app.on_message(filters.command(["anime"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def anilist_anime_search(_, message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("**ɢɪᴠᴇ ᴀɴ ᴀɴɪᴍᴇ ᴛɪᴛʟᴇ ғᴏʀ sᴇᴀʀᴄʜ 🔍**")

    query_str = '''
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        title {
          romaji
          english
          native
        }
        coverImage {
          large
        }
      }
    }
    '''
    variables = {
        'search': query
    }
    response = requests.post(ANILIST_API_URL, json={'query': query_str, 'variables': variables})
    data = response.json()

    if 'errors' in data:
        return await message.reply(f"**sᴇᴀʀᴄʜ ғᴀɪʟᴇᴅ:** {data['errors'][0]['message']}")

    media = data.get('data', {}).get('Media', {})
    cover_url = media.get('coverImage', {}).get('large')

    if not cover_url:
        return await message.reply("**ɴᴏ ɪᴍᴀɢᴇs ғᴏᴜɴᴅ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ʏᴏᴜʀ qᴜᴇʀʏ.**")

    media_group = [InputMediaPhoto(media=cover_url)]

    try:
        await app.send_media_group(
            chat_id=chat_id,
            media=media_group,
            reply_to_message_id=message.id
        )
    except Exception as e:
        await message.reply(f"**ᴇʀʀᴏʀ:** {e}")
