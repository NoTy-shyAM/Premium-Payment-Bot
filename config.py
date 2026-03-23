import os
import logging

logging.basicConfig(
    format="%(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Credentials
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8752309188:AAFwEnnK1FF_4HsNN9Obc1Y4lFxqkL20cQM")
API_ID = int(os.environ.get("API_ID", "39962714"))
API_HASH = os.environ.get("API_HASH", "f8e944ea9d9382fe91efaa29fc2584aa")

ADMIN_ID = int(os.environ.get("ADMIN_ID", 8562617924))
ADMIN_IDs = [8562617924]

# Channels
fsub_id = int(os.environ.get("fsub_id", "-1003871462746"))
FORCE_SUBSCRIBE = True
furl = "https://t.me/DbinUpdate"

demo_id = int(os.environ.get("demo_id", "-1003421895942"))
message_iid = [3, 4, 5, 6, 7]
ENG_VOD = int(os.environ.get("ENG_VOD", "-1003191158357"))
ALL_VOD = int(os.environ.get("ALL_VOD", "-1003427751079"))

# Global Variables (Jo pluginsv ki files dhoondh rahi hain)
SUPPORT_ADMIN = "https://t.me/arun_0116"
rate1 = "399"
rate2 = "699"
day1 = "30"
day2 = "60"

# Buttons
BTN_VIP_CPS = "💥VIP CPs Vid£S🤤"
BTN_VIP_VIRAL = "💥C/P Mix Videos🤤"
BTN_MY_PLAN = "My Plan"
BTN_GET_HELP = "Get Help🧑‍💻"

# Messages
MSG_PREMIUM_USER = """**<blockquote>Hᴇʏ! {user_mention},</blockquote>
You are a premium user. You can use all features of this bot without any restrictions.
You can Watch Unlimited video Without any Link and Ads.

Share and Support Us.**"""

MSG_WELCOME = """**
<blockquote>Hᴇʏ! {user_mention},

Welcome to Premium Video Bot</blockquote>

Benefits of premium
📍No Ads ✅
📍Direct Video ✅
📍No link✅

Content type  (50+video/daily)
CP Videos 🤤
Mix cp videos 🔫
All leaks video available 😁**"""

MSG_PRICING = """**
Monthly recharge price

  ₹{rate1} / {day1} days 😄
  ₹{rate2} / {day2} days 😄

Payment method👇
📍Gpay Phonepay, Upi or Paytm
Amazon pay or any other upi app**"""

MSG_DEMO_CAPTION = "**Demo video for you\nYou'll get these all videos**"
MSG_VIDEO_LIMIT = "**You have reached the maximum limit of 2 videos. \n\nPlease upgrade your plan to get Unlimited videos**"
MSG_FAILED_VIDEO = "Failed to get video. Please try again."
MSG_FAILED_VIDEOS = "Failed to get videos. Please try again."

# Default Config dictionary (Agar koi aur file isey maange toh)
DEFAULT_CONFIG = {
    "SUPPORT_ADMIN": SUPPORT_ADMIN,
    "rate1": rate1,
    "rate2": rate2,
    "day1": day1,
    "day2": day2,
    "FORCE_SUBSCRIBE": FORCE_SUBSCRIBE,
    "fsub_id": fsub_id,
    "furl": furl,
    "demo_id": demo_id,
    "message_iid": message_iid,
    "ENG_VOD": ENG_VOD,
    "ALL_VOD": ALL_VOD,
    "BTN_VIP_CPS": BTN_VIP_CPS,
    "BTN_VIP_VIRAL": BTN_VIP_VIRAL,
    "BTN_MY_PLAN": BTN_MY_PLAN,
    "BTN_GET_HELP": BTN_GET_HELP,
    "MSG_PREMIUM_USER": MSG_PREMIUM_USER,
    "MSG_WELCOME": MSG_WELCOME,
    "MSG_PRICING": MSG_PRICING,
    "MSG_DEMO_CAPTION": MSG_DEMO_CAPTION,
    "MSG_VIDEO_LIMIT": MSG_VIDEO_LIMIT,
    "MSG_FAILED_VIDEO": MSG_FAILED_VIDEO,
    "MSG_FAILED_VIDEOS": MSG_FAILED_VIDEOS,
}