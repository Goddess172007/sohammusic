import urllib.request
from pymongo import ReturnDocument
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, sudo_users, collection, db, CHARA_CHANNEL_ID, SUPPORT_CHAT

import logging

logging.basicConfig(level=logging.INFO)

WRONG_FORMAT_TEXT = """Wrong ❌️ format...  eg. /upload Img_url muzan-kibutsuji Demon-slayer 3

img_url character-name anime-name rarity-number

use rarity number accordingly rarity Map

rarity_map = 1 (⚪️ Common), 2 (🟣 Rare) , 3 (🟡 Legendary), 4 (🟢 Medium), 5 (💮 Special Edition), 6 (🔮 Limited Edition), 9 (🎐 Celestial), 10 (❄️ Winter), 12 (💝 Valentine), 15(💸 Premium Edition)"""

rarity_map = {
    1: "⚪ Common",
    2: "🟣 Rare",
    3: "🟡 Legendary",
    4: "🟢 Medium",
    5: "💮 Special Edition",
    6: "🔮 Limited Edition",
    9: "🎐 Celestial",
    10:"❄️ Winter", 
    12: "💝 Valentine",
    15: "💸 Premium Edition"
}

async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name}, 
        {'$inc': {'sequence_value': 1}}, 
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return 0
    return sequence_document['sequence_value']

async def validate_url(url):
    try:
        urllib.request.urlopen(url)
        return True
    except:
        return False

async def handle_upload(update: Update, context: CallbackContext):
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask My Owner...')
        return

    try:
        args = context.args
        if len(args) != 4:
            await update.message.reply_text(WRONG_FORMAT_TEXT)
            return

        img_url, character_name, anime_name, rarity_number = args

        character_name = character_name.replace('-', ' ').title()
        anime_name = anime_name.replace('-', ' ').title()

        if not await validate_url(img_url):
            await update.message.reply_text('Invalid URL.')
            return

        try:
            rarity = rarity_map[int(rarity_number)]
        except KeyError:
            await update.message.reply_text('Invalid rarity. Please use a valid number according to the rarity map.')
            return

        character_id = str(await get_next_sequence_number('character_id')).zfill(2)

        character = {
            'img_url': img_url,
            'name': character_name,
            'anime': anime_name,
            'rarity': rarity,
            'id': character_id
        }

        try:
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=img_url,
                caption=(
                    f'<b>Character Name:</b> {character_name}\n'
                    f'<b>Anime Name:</b> {anime_name}\n'
                    f'<b>Rarity:</b> {rarity}\n'
                    f'<b>ID:</b> {character_id}\n'
                    f'Added by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>'
                ),
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.insert_one(character)
            await update.message.reply_text('Character added successfully.')
        except Exception as e:
            await collection.insert_one(character)
            logging.error(f"Error sending photo to channel: {e}")
            await update.message.reply_text('Character added to database but not posted to channel.')

    except Exception as e:
        logging.error(f"Upload error: {e}")
        await update.message.reply_text(f'Character upload unsuccessful. Error: {str(e)}\nIf you think this is a source error, forward to: {SUPPORT_CHAT}')

async def handle_delete(update: Update, context: CallbackContext):
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask my Owner to use this Command...')
        return

    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text('Incorrect format... Please use: /delete ID')
            return

        character_id = args[0]
        character = await collection.find_one_and_delete({'id': character_id})

        if character:
            try:
                await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
                await update.message.reply_text('Character deleted successfully.')
            except Exception as e:
                logging.error(f"Error deleting message from channel: {e}")
                await update.message.reply_text('Deleted from database, but not found in channel.')
        else:
            await update.message.reply_text('Character not found in database.')
    except Exception as e:
        logging.error(f"Delete error: {e}")
        await update.message.reply_text(f'Error: {str(e)}')

async def handle_update(update: Update, context: CallbackContext):
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('You do not have permission to use this command.')
        return

    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text('Incorrect format. Please use: /update id field new_value')
            return

        character_id, field, new_value = args

        character = await collection.find_one({'id': character_id})
        if not character:
            await update.message.reply_text('Character not found.')
            return

        if field not in ['img_url', 'name', 'anime', 'rarity']:
            await update.message.reply_text(f'Invalid field. Please use one of the following: img_url, name, anime, rarity.')
            return

        if field == 'rarity':
            try:
                new_value = rarity_map[int(new_value)]
            except KeyError:
                await update.message.reply_text('Invalid rarity. Please use a valid number according to the rarity map.')
                return
        elif field in ['name', 'anime']:
            new_value = new_value.replace('-', ' ').title()

        await collection.find_one_and_update({'id': character_id}, {'$set': {field: new_value}})

        if field == 'img_url':
            try:
                await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
                message = await context.bot.send_photo(
                    chat_id=CHARA_CHANNEL_ID,
                    photo=new_value,
                    caption=(
                        f'<b>Character Name:</b> {character["name"]}\n'
                        f'<b>Anime Name:</b> {character["anime"]}\n'
                        f'<b>Rarity:</b> {character["rarity"]}\n'
                        f'<b>ID:</b> {character["id"]}\n'
                        f'Updated by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>'
                    ),
                    parse_mode='HTML'
                )
                await collection.find_one_and_update({'id': character_id}, {'$set': {'message_id': message.message_id}})
            except Exception as e:
                logging.error(f"Error updating image in channel: {e}")
        else:
            try:
                await context.bot.edit_message_caption(
                    chat_id=CHARA_CHANNEL_ID,
                    message_id=character['message_id'],
                    caption=(
                        f'<b>Character Name:</b> {character["name"]}\n'
                        f'<b>Anime Name:</b> {character["anime"]}\n'
                        f'<b>Rarity:</b> {character["rarity"]}\n'
                        f'<b>ID:</b> {character["id"]}\n'
                        f'Updated by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>'
                    ),
                    parse_mode='HTML'
                )
            except Exception as e:
                logging.error(f"Error updating caption in channel: {e}")

        await update.message.reply_text('Update completed successfully.')
    except Exception as e:
        logging.error(f"Update error: {e}")
        await update.message.reply_text('Update unsuccessful. Ensure the bot is added to the channel or the character exists.')

UPLOAD_HANDLER = CommandHandler('upload', handle_upload, block=False)
application.add_handler(UPLOAD_HANDLER)
DELETE_HANDLER = CommandHandler('delete', handle_delete, block=False)
application.add_handler(DELETE_HANDLER)
UPDATE_HANDLER = CommandHandler('update', handle_update, block=False)
application.add_handler(UPDATE_HANDLER)
