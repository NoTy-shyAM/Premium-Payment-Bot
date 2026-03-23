import os, sys
from pyrogram import Client, filters
from config import logger, ADMIN_IDs, BTN_VIP_CPS, BTN_VIP_VIRAL, BTN_MY_PLAN, BTN_GET_HELP

# Aapke baaki files se functions import kar rahe hain
from pluginsv.mo import pay_c, pay_b, check_payment_status, support_admin, set_bot_commands
from pluginsv.vid import start, demo_video_callback, send_platform_video
from pluginsv.pd import my_plan

# Yahan @Client hona zaroori hai plugin load hone ke liye
@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    await start(client, message)

@Client.on_message(filters.regex(BTN_VIP_CPS) | filters.regex(BTN_VIP_VIRAL))
async def video_handler(client, message):
    await send_platform_video(client, message)

@Client.on_message(filters.regex(BTN_MY_PLAN))
async def plan_handler(client, message):
    await my_plan(client, message)
    
@Client.on_message(filters.command("buy"))
async def buy_handler(client, message):
    await pay_c(client, message)
    
@Client.on_callback_query(filters.regex("^pay_"))
async def pay_callback(client, query):
    await pay_b(client, query)

@Client.on_callback_query(filters.regex("^check_payment_status_"))
async def check_payment_callback(client, query):
    await check_payment_status(client, query)

@Client.on_callback_query(filters.regex("^DemoVideos$"))
async def demo_handler(client, query):
    from pluginsv.vid import demo_video_callback
    await demo_video_callback(client, query)

@Client.on_callback_query(filters.regex("^buy_plan$"))
async def buy_plan_callback(client, query):
    from pluginsv.mo import pay_c
    # Query ke message ko user ka message bana kar bhejenge taaki error na aaye
    query.message.from_user = query.from_user 
    await pay_c(client, query.message)