from pymongo import MongoClient
import os

# Naya URL jo aapke naye cluster ka hai
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "mongodb+srv://premiumbot:Prem1234@cluster0.gkxt3ps.mongodb.net/?appName=Cluster0",
)

DATABASE_NAME = os.environ.get("DATABASE_NAME", "premium_bot_db")

client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]
users_collection = db["users"]
timer_collection = db["timer"]
config_collection = db["config"]