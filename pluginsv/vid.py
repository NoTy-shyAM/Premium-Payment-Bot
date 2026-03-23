import asyncio
import random
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    ENG_VOD, ALL_VOD, BTN_VIP_CPS, BTN_VIP_VIRAL, BTN_MY_PLAN, BTN_GET_HELP,
    MSG_VIDEO_LIMIT, MSG_FAILED_VIDEO, logger, MSG_WELCOME, MSG_DEMO_CAPTION, message_iid, demo_id
)
from pluginsv.pd import is_pro
from sett import SETTINGS_CACHE

# YAHAN MEMORY STORE HOGI
USER_PROGRESS = {}

# --- Video Bhejne Wala Main Function ---
async def send_platform_video(client, message):
    user_id = message.from_user.id
    platform = message.text
    
    # 1. Premium Check
    premium = await is_pro(user_id)
    if not premium:
        return await message.reply_text(
            "❌ **Free trial limit reached!**\nUnlimited videos dekhne ke liye Premium lijiye.", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("• Bᴜʏ Pʀᴇᴍɪᴜᴍ💸", callback_data="buy_plan")]])
        )

    # 2. Channel Set Karna
    if platform == BTN_VIP_CPS:
        channel_id = ENG_VOD
        cache_key = "max_range_channel_1"
    else:
        channel_id = ALL_VOD
        cache_key = "max_range_channel_2"
        
    max_range = SETTINGS_CACHE.get(cache_key, 0)
    
    # Failsafe: Agar range 0 aaye toh 8000 maan lega
    if max_range < 50:
        max_range = 8000

    status_msg = await message.reply_text("⏳ **Videos dhoondh raha hoon, kripya wait karein...**")

    # 3. SUPER FAST FETCH LOGIC: Ek sath 50 random IDs uthao
    random_ids = random.sample(range(2, max_range + 1), 50)
    sent_count = 0

    try:
        msgs = await client.get_messages(channel_id, random_ids)
        for msg in msgs:
            # Check karein ki message khali na ho aur usme video ho
            if msg and not msg.empty and (msg.video or msg.document):
                try:
                    await msg.copy(chat_id=user_id, protect_content=True)
                    sent_count += 1
                    await asyncio.sleep(0.5) # Telegram Ban se bachne ke liye
                    
                    if sent_count >= 10: # 10 videos hote hi loop band
                        break
                except Exception:
                    continue
    except Exception as e:
        logger.error(f"Error: {e}")

    # 4. Final Report
    if sent_count > 0:
        await status_msg.edit_text(f"✅ **{sent_count} Videos successfully bhej di gayi hain!**\n\nNiche button dabane par agli nayi videos aayengi.")
    else:
        await status_msg.edit_text("❌ **Maaf karna, aage koi video nahi mili!**\nYa toh videos khatam ho gayi hain, ya channel se delete ho gayi hain.")

# --- Start Command ---
async def start(client, message):
    user_mention = message.from_user.mention
    
    main_keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton(BTN_VIP_CPS), KeyboardButton(BTN_VIP_VIRAL)],
            [KeyboardButton(BTN_MY_PLAN), KeyboardButton(BTN_GET_HELP)]
        ],
        resize_keyboard=True
    )
    
    inline_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("• Bᴜʏ Pʀᴇᴍɪᴜᴍ💸", callback_data="buy_plan")],
        [InlineKeyboardButton("Demo Videos", callback_data="DemoVideos")]
    ])
    
    await message.reply_text(MSG_WELCOME.format(user_mention=user_mention), reply_markup=main_keyboard)
    await message.reply_text("👇 **Premium aur Demo ke liye niche click karein:**", reply_markup=inline_kb)

# --- Demo Video Command ---
async def demo_video_callback(client, query):
    await query.message.delete()
    for m_id in message_iid:
        try:
            await client.copy_message(query.from_user.id, demo_id, m_id, caption=MSG_DEMO_CAPTION)
            await asyncio.sleep(1)
        except:
            pass

# --- Admin Range Commands ---
async def set_channel_range(client, message):
    cmd = message.command
    if len(cmd) < 2: return
    val = int(cmd[1])
    if cmd[0] == "r1": SETTINGS_CACHE["max_range_channel_1"] = val
    if cmd[0] == "r2": SETTINGS_CACHE["max_range_channel_2"] = val
    await message.reply_text(f"✅ Range updated to {val}")

async def settings_status(client, message):
    await message.reply_text(f"⚙️ **Status:**\nRange 1: {SETTINGS_CACHE.get('max_range_channel_1', 0)}\nRange 2: {SETTINGS_CACHE.get('max_range_channel_2', 0)}")

async def show_ranges(client, message):
    await message.reply_text(str(SETTINGS_CACHE))