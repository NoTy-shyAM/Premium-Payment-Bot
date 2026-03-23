from pyrogram.errors import UserNotParticipant, ChatAdminRequired, FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from config import ADMIN_ID, fsub_id, logger, furl
import asyncio, traceback
from db import users_collection

async def is_user_member(client, user_id, channel_id):
    try:
        member = await client.get_chat_member(channel_id, user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except UserNotParticipant:
        return False
    except ChatAdminRequired:
        logger.error(f"Bot does not have admin rights in the channel: {channel_id}")
        try:
            await client.send_message(ADMIN_ID, f"**Please add me as an admin in the channel: `{channel_id}`**")
        except Exception as e:
            logger.error(f"Failed to send message to admin: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"An error occurred while checking membership for user {user_id} in channel {channel_id}: {str(e)}")
        return False

async def enforce_subscription(client, message):
    user_id = message.from_user.id
    channel_1_id = fsub_id
    is_member_1 = await is_user_member(client, user_id, channel_1_id)
    logger.info(f"User {user_id} membership status: Channel 1: {is_member_1}")
    if not (is_member_1):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url=furl)]
        ])
        await message.reply_photo(
            photo="https://i.ibb.co/qRdLnNn/2025-01-13-Text-Studio.png",
            caption="""**<blockquote>Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ ᴛʜᴇɴ Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ Jᴏɪɴ ᴍʏ ᴀʟʟ Cʜᴀɴɴᴇʟs\n\nअगर आप इस Bot को का प्रयोग करना चाहते हो तो सबसे पहले नीचे के सभी channels को जॉइन करो तब use करना.</blockquote>**""",
            reply_markup=keyboard
        )
        return False
    return True

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid) as e:
        raise e  # Raise to handle in broadcast for deletion
    except Exception as e:
        logger.error(f"Unexpected error: {traceback.format_exc()}")
        raise e  # For any unexpected exception

async def broadcast(client, message):
    if not message.reply_to_message:
        await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ɪᴛ.**")
        return

    await message.reply_text("**sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ!**")
    all_users = users_collection.find({})
    done_users = 0
    failed_users = 0
    failed_users_ids = []

    for user_data in all_users:
        user_id = user_data["_id"]
        try:
            await send_msg(user_id, message.reply_to_message)
            done_users += 1
            await asyncio.sleep(0.1)
        except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
            # If user didn't accept or deactivated, add them to deletion list
            failed_users += 1
            failed_users_ids.append(user_id)
        except Exception as e:
            failed_users += 1
            failed_users_ids.append(user_id)
            logger.error(f"Failed to send message to {user_id}: {traceback.format_exc()}")
    if failed_users_ids:
        try:
            non_pro_users_ids = [user_id for user_id in failed_users_ids if not users_collection.find_one({"_id": user_id, "plan_name": "Pro"})]
            if non_pro_users_ids:
                users_collection.delete_many({"_id": {"$in": non_pro_users_ids}})
                logger.info(f"Deleted {len(non_pro_users_ids)} users from the database due to broadcast errors.")
        except Exception as e:
            logger.error(f"Failed to delete users from database: {traceback.format_exc()}")

    if failed_users == 0:
        await message.reply_text(
            f"**sᴜᴄᴄᴇssғᴜʟʟʏ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ✅**\n\n**sᴇɴᴛ ᴍᴇssᴀɢᴇ ᴛᴏ** `{done_users}` **ᴜsᴇʀs**",
        )
    else:
        await message.reply_text(
            f"**sᴜᴄᴄᴇssғᴜʟʟʏ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ✅**\n\n**sᴇɴᴛ ᴍᴇssᴀɢᴇ ᴛᴏ** `{done_users}` **ᴜsᴇʀs**\n\n",
        )