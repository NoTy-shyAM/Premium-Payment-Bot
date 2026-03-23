from db import users_collection, timer_collection
from datetime import datetime
from config import logger, ENG_VOD, ALL_VOD
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

SETTINGS_CACHE = {
    "max_range_channel_1": 500,
    "max_range_channel_2": 500,
}

async def get_max_range_from_channel(client, channel_id):
    try:
        # Bot channel mein test karke max range nikalega
        message = await client.send_message(channel_id, "This is a test message Kindly ignore it.")
        await message.delete()
        return message.id
    except Exception as e:
        logger.error(f"Error getting max range from channel {channel_id}: {str(e)}")
        # FAILSAFE FIX: Agar bot admin nahi hai, toh 0 nahi, 8000 return karega taaki videos aati rahein!
        return 8000

async def update_max_ranges(client):
    global SETTINGS_CACHE
    SETTINGS_CACHE["max_range_channel_1"] = await get_max_range_from_channel(client, ENG_VOD)
    SETTINGS_CACHE["max_range_channel_2"] = await get_max_range_from_channel(client, ALL_VOD)
    logger.info("Max ranges updated successfully!")

async def load_settings_cache(client):
    global SETTINGS_CACHE
    while True:
        if client:
            await update_max_ranges(client)
        logger.info(f"Settings cache loaded: {SETTINGS_CACHE}")
        await asyncio.sleep(7200)

Pro_user_ids = []