from datetime import datetime, timedelta
from db import users_collection
from config import logger

# 1. User ko premium banane ka function (Payment success hone par)
async def pro_user_d(client, user_id, days):
    try:
        expiry_date = datetime.now() + timedelta(days=days)
        users_collection.update_one(
            {"_id": user_id},
            {"$set": {
                "is_pro": True, 
                "expiry_date": expiry_date,
                "plan_days": days
            }},
            upsert=True
        )
        logger.info(f"User {user_id} upgraded to Pro for {days} days.")
        await client.send_message(
            user_id, 
            f"🎊 **Congratulations!**\nAapka **{days} Days** ka Premium plan activate ho gaya hai.\nAb aap bina kisi limit ke videos dekh sakte hain!"
        )
    except Exception as e:
        logger.error(f"Error in pro_user_d: {e}")

# 2. YEH RAHA MISSING FUNCTION - Yeh check karega user premium hai ya nahi
async def is_pro(user_id):
    user = users_collection.find_one({"_id": user_id})
    if user and user.get("is_pro"):
        expiry = user.get("expiry_date")
        if expiry and expiry > datetime.now():
            return True
        else:
            # Plan expire ho gaya toh false kar do
            users_collection.update_one({"_id": user_id}, {"$set": {"is_pro": False}})
    return False

# 3. User ko apna plan dekhne ke liye (/myplan)
async def my_plan(client, message):
    user_id = message.from_user.id
    user = users_collection.find_one({"_id": user_id})
    
    if user and user.get("is_pro"):
        expiry = user.get("expiry_date").strftime('%d-%m-%Y')
        await message.reply_text(f"🌟 **Your Plan:** Premium\n📅 **Expiry:** {expiry}\n🚀 **Status:** Unlimited Access")
    else:
        await message.reply_text("❌ Aapke paas koi active premium plan nahi hai.\nPremium lene ke liye 'Buy Premium' par click karein.")

# 4. Admin manual command - kisi ko free mein premium dene ke liye (/auth)
async def pro_user(client, message):
    if len(message.command) < 3:
        return await message.reply_text("Usage: `/auth [user_id] [days]`")
    try:
        uid = int(message.command[1])
        days = int(message.command[2])
        await pro_user_d(client, uid, days)
        await message.reply_text(f"✅ User `{uid}` ko {days} din ke liye pro bana diya gaya hai.")
    except:
        await message.reply_text("❌ Sahi User ID aur Days daalein.")

# 5. Admin command - kisi ka premium hatane ke liye (/remove)
async def remove_subscription(client, message):
    try:
        uid = int(message.command[1])
        users_collection.update_one({"_id": uid}, {"$set": {"is_pro": False}})
        await message.reply_text(f"❌ User `{uid}` ka premium hata diya gaya hai.")
    except:
        pass

# 6. Bot ke stats dekhne ke liye (/stats)
async def get_stats(client, message):
    total = users_collection.count_documents({})
    pro = users_collection.count_documents({"is_pro": True})
    await message.reply_text(f"📊 **Bot Stats:**\nTotal Users: {total}\nPremium Users: {pro}")