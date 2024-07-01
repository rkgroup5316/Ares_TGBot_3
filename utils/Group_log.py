from telegram.ext import ContextTypes
from telegram import Update
from config import LOGGER_CHATID
from telegram.constants import ParseMode
from datetime import datetime






async def LOG(update: Update,context: ContextTypes.DEFAULT_TYPE , msg :str) -> str:
    """
    LOGs the msg to the log group
    of admin cmd
    
    """
    user = update.effective_user
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    formatted_message = (
        f"<b>Dᴀᴛᴇ:</b> <i>{current_date}</i>\n"
        f"<b>Iɴɪᴛɪᴀᴛᴇᴅ ʙʏ:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
        f"<b>Lᴏɢ:</b>\n\n {msg}"
    )

     # Finally, send the message
    await context.bot.send_message(
        chat_id=LOGGER_CHATID, text=formatted_message, parse_mode=ParseMode.HTML
    )



