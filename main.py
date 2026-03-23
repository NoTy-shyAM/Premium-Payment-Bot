import asyncio

# Pyrogram import hone se PEHLE humein loop set karna hoga naye Python ke liye
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from config import API_HASH, API_ID, BOT_TOKEN, logger, ADMIN_ID
from pyrogram import Client, idle

plugins = dict(root="pluginsv")

async def start_bot():
    bot = Client(
        "bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins # Ye line zaroori hai
)
    
    await bot.start()
    bot_info = await bot.get_me()
    print(f"✅ Bot Started as @{bot_info.username}")
    print("=========================================")
    print("      BOT PROUDLY RUN BY @arun_0116      ")
    print("=========================================")

    try:
        await bot.send_message(ADMIN_ID, "**Bot Started Successfully!**")
    except:
        pass
        
    await idle()
    await bot.stop()

if __name__ == "__main__":
    loop.run_until_complete(start_bot()) 