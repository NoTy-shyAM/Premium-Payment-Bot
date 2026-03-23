import os, random, qrcode, requests, asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from pluginsv.pd import pro_user_d
from db import timer_collection
from config import ADMIN_ID, SUPPORT_ADMIN

# Ankush ki sahi API URL
GATEWAY_URL = "https://mswpresents.koyeb.app/api/paytm-gateway" 

# Naye Plans jo aapne mange
pay_button = InlineKeyboardMarkup([
    [InlineKeyboardButton("₹399 - 30 Days", callback_data="pay_399|30")],
    [InlineKeyboardButton("₹699 - 60 Days", callback_data="pay_699|60")]
])

async def pay_b(client, query):
    await query.message.delete(True)
    user_id = query.from_user.id
    user_mention = query.from_user.mention
    
    settings = timer_collection.find_one({"_id": "settings"})
    # MongoDB se Business ID uthayega
    upi = settings.get("upi_id") 
    
    try:
        data_parts = query.data.split("_")[1].split("|")
        amount, days = int(data_parts[0]), int(data_parts[1])
    except:
        return await query.answer("❌ Invalid plan selection.", show_alert=True)
    
    # Nayi Order ID generate karna
    order_id = f"{random.randint(111111111, 999999999)}"
    qr_data = f"upi://pay?pa={upi}&pn=DINESH%20KUMAR&am={amount}&tr={order_id}&tn={user_id}-dirdinesh"
    
    temp_dir = 'temp/'
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    qr_path = os.path.join(temp_dir, f"{order_id}.png")
    qrcode.make(qr_data).save(qr_path)

    # Verify Button jo aapne manga tha
    verify_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Verify Payment", callback_data=f"check_payment_status_{order_id}_{days}")]
    ])

    caption = (f"**Hey {user_mention}, Welcome!**\n\n"
               f"💰 Amount: `₹{amount}`\n"
               f"⏳ Plan: `{days} Days`\n"
               f"🔖 Order ID: `{order_id}`\n\n"
               f"👆 **Scan & Pay. Payment hone ke baad niche verify button dabayein.**")

    msg = await client.send_photo(chat_id=user_id, photo=qr_path, caption=caption, reply_markup=verify_kb)
    if os.path.exists(qr_path): os.remove(qr_path)
    
    # Auto-Verification Task
    asyncio.create_task(periodic_payment_check(client, msg, user_id, order_id, days))

async def periodic_payment_check(client, msg, user_id, order_id, days):
    for _ in range(60): 
        await asyncio.sleep(5)
        status = verify_payment(order_id)
        if status and status.get("STATUS") == "TXN_SUCCESS":
            await msg.delete()
            await pro_user_d(client, user_id, days)
            await client.send_message(user_id, f"✅ **Payment Success!**\n\nPremium Activated for {days} days.")
            await client.send_message(ADMIN_ID, f"💰 Success: ₹{status.get('TXNAMOUNT')} from `{user_id}`")
            return
    
    await msg.edit_caption("⚠️ **QR Expired!** Niche click karke check karein.", 
                           reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Verify Payment", callback_data=f"check_payment_status_{order_id}_{days}")]]))

def verify_payment(order_id):
    settings = timer_collection.find_one({"_id": "settings"})
    m_id = settings.get("merchant_id")
    # API Verification logic
    params = {"merchant_id": m_id, "orderid": order_id}
    headers = {"host": "mswpresents.koyeb.app"}
    try:
        res = requests.get(GATEWAY_URL, headers=headers, params=params).json()
        if res.get("success") == True and res.get("STATUS") == "TXN_SUCCESS":
            return res
    except: return False
    return False

async def check_payment_status(client, query):
    data = query.data.split("_")
    order_id, days = (data[3], int(data[4])) if len(data) > 3 else (data[1], int(data[2]))
    status = verify_payment(order_id)
    if status and status.get("STATUS") == "TXN_SUCCESS":
        await query.message.delete()
        await pro_user_d(client, query.from_user.id, days)
        await query.answer("✅ Success! Premium Activated.", show_alert=True)
    else:
        await query.answer("❌ Abhi payment nahi mili!", show_alert=True)

# Missing Support function jiski wajah se error aa raha tha
async def support_admin(client, message):
    await message.reply_text(f"**Kaise ho bhai? Support ke liye yahan contact karein:**\n{SUPPORT_ADMIN}")

async def pay_c(client, message):
    await message.reply_text("Ek plan select karein:", reply_markup=pay_button)

async def set_bot_commands(client, message):
    await client.set_bot_commands([BotCommand("start", "Check Bot"), BotCommand("buy", "Purchase Plan")])
    await message.reply_text("✅ Commands set ho gaye!")