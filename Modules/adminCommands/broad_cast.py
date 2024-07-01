from utils.log import logger
from utils.dataBase.FireDB import DB
from telegram.constants import ParseMode
from assets.assets import load_asset
from config import WARN_USERS,LOADING_BAR
from utils.decoders_ import IsAdmin
from assets.assets import load_asset
from Modules.inline import CLOSE_BUTTON
from utils.Group_log import LOG
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)

@IsAdmin
async def GB_broadCast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat_id = update.effective_message.chat_id
    if message.reply_to_message:
            
        msg = await update.message.reply_photo(photo=load_asset(LOADING_BAR),caption="Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜsᴇʀ...")
        logger.info(f"{update.effective_user.first_name},Started a Global BroadCast ")
        original_message = message.reply_to_message
        userIds = DB.get_usernames()
        for user_id in userIds:
           
                
            try:
                await context.bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=original_message.chat_id,
                    message_id=original_message.message_id, 
                ) 
            except Exception as e:
                logger.error(f"Error sending message to chat ID {user_id}: {e}")
                if "bot was blocked by the user" in str(e):
                    logger.info(f"Skipping user {user_id} as they have blocked the bot.")
                else:
                    await context.bot.send_message(chat_id=chat_id, text=f"Error sending message to chat ID {user_id}: {e}", parse_mode=ParseMode.HTML)
        
        try:
            msg_Log = f"<b>📢 Gʟᴏʙᴀʟ Bʀᴏᴀᴅᴄᴀsᴛ</b>\n<b>>ᴍsɢIᴅ:</b><code>{message.id}\n</code><b>ChatID:</b>:<code>{message.chat_id}</code>"
            await LOG(update,context,msg_Log)
        
        except Exception as e:
            logger.error(f"An Error occureed while Logging global brodacast error: {e}")
    
        await msg.edit_caption(caption=f"Bʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ🎉🎉.\n\nTotal Chats: {len(userIds)}",parse_mode="HTML",reply_markup=CLOSE_BUTTON)

    else:
        await context.bot.send_message(chat_id=chat_id, text="Please reply to a message to broadcast it.")

@IsAdmin
async def SP_broadCast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat_id = update.effective_message.chat_id

    args = context.args
    if not args:
        await update.message.reply_text("Usᴀɢᴇ: /sᴘ_ʙʀᴏᴀᴅᴄᴀsᴛ (ᴄʜᴀᴛ_ɪᴅ)")
        return

    if message.reply_to_message:
            
        msg = await update.message.reply_photo(photo=load_asset(LOADING_BAR),caption="Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴇssᴀɢᴇ ᴛᴏ ᴜsᴇʀ...")
        logger.info(f"{update.effective_user.first_name},Did a specific broadcast to UserId: {args}")

        original_message = message.reply_to_message
        userIds = args
        for user_id in userIds:
           
                
            try:
                await context.bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=original_message.chat_id,
                    message_id=original_message.message_id, 
                ) 
                
            except Exception as e:
                logger.error(f"Error sending message to chat ID {user_id}: {e}")
                if "bot was blocked by the user" in str(e):
                    logger.info(f"Skipping user {user_id} as they have blocked the bot.")
                else:
                    await context.bot.send_message(chat_id=chat_id, text=f"Error sending message to chat ID {user_id}: {e}", parse_mode=ParseMode.HTML)

        try:
            msg_Log = f"<b>📢 Sᴘᴇᴄɪғɪᴄ Bʀᴏᴀᴅᴄᴀsᴛ</b>\n<b>>ᴍsɢIᴅ:</b><code>{message.id}\n</code><b>Fʀᴏᴍ ChatID: </b><code>{message.chat_id}</code>\n<b>Tᴏ CʜᴀᴛIᴅ: {args} </b> "
            await LOG(update,context,msg_Log)
        
        except Exception as e:
            logger.error(f"An Error occureed while Logging specific brodacast error: {e}")
    
                
        await msg.edit_caption(caption="Bʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ🎉🎉.",reply_markup=CLOSE_BUTTON)

    else:
        await context.bot.send_message(chat_id=chat_id, text="Please reply to a message to broadcast it.")


@IsAdmin
async def Warn_Users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id

    args = context.args
    if not args:
        await update.message.reply_text("Usᴀɢᴇ: /warn (ᴄʜᴀᴛ_ɪᴅ)")
        return
    msg = await update.message.reply_photo(photo=load_asset(LOADING_BAR),caption=f"Sending warning to: {args} .... ")
    logger.info(f"{update.effective_user.first_name},Did a warn  to UserId: {args}")

    userIds = args
    warning_message = """
<b>Official Warning Notice</b>

Dear User,

It has come to our attention that your recent behavior in our community has violated our community guidelines. We take such matters very seriously to ensure a positive and respectful environment for all members.

<i>This is an official warning issued by the administrators of the Ares community. Continued inappropriate behavior may result in further action, including but not limited to temporary or permanent suspension from the community.</i>

If you have any questions or believe this warning was issued in error, please reach out to our support team for assistance. You can contact us via our support chat by clicking <a href='https://t.me/AresChatBotAi'>ARES</a>.

Thank you for your attention to this matter and for your cooperation in maintaining a respectful community.

Sincerely,

The Ares Administration Team
"""

    for user_id in userIds:
           
                
        try:
            await context.bot.send_photo(
                    chat_id=user_id,
                    photo=load_asset(WARN_USERS),
                    caption=warning_message,
                    parse_mode="HTML"

                     
                ) 
                
        except Exception as e:
            logger.error(f"Error sending message to chat ID {user_id}: {e}")
            if "bot was blocked by the user" in str(e):
                logger.info(f"Skipping user {user_id} as they have blocked the bot.")
            else:
                await context.bot.send_message(chat_id=chat_id, text=f"Error sending message to chat ID {user_id}: {e}", parse_mode=ParseMode.HTML)
    
        try:
            msg_Log = f"<b>📢 ᴡᴀʀɴ Bʀᴏᴀᴅᴄᴀsᴛ</b>\n<b>>ᴍsɢIᴅ:</b><code>{update.message.id}\n</code><b>Fʀᴏᴍ ChatID: </b><code>{update.message.chat_id}</code>\n<b>Tᴏ CʜᴀᴛIᴅ: {args} </b> "
            await LOG(update,context,msg_Log)
        
        except Exception as e:
            logger.error(f"An Error occureed while Logging specific brodacast error: {e}")
    
             
        await msg.edit_caption(caption="warning Bʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ🎉🎉.",reply_markup=CLOSE_BUTTON)




Global_BROADCAST = CommandHandler(("gb_broadcast","global_broadcast","GbBroadcast","GlobalBroadCast"),GB_broadCast)
Specific_BROADCAST = CommandHandler(("sp_broadcast","specific_broadcast","sms"),SP_broadCast)
WARN_USER_BROADCAST = CommandHandler("warn",Warn_Users)