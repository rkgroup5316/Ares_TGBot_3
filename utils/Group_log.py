from telegram.ext import ContextTypes
from telegram import Update
from config import LOGGER_CHATID
from telegram.constants import ParseMode
from datetime import datetime


async def LOG(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str, level: str = "INFO") -> None:
    """
    Logs a message to the admin log group with enhanced formatting.
    
    Args:
        update: The telegram update object
        context: The telegram context object
        msg: The message to log
        level: Log level (INFO, WARNING, ERROR, SUCCESS)
    
    Returns:
        None
    """
    # Get user information safely
    user = update.effective_user
    user_mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>" if user else "Unknown User"
    
    # Get chat information
    chat = update.effective_chat
    chat_info = ""
    if chat:
        chat_title = chat.title or chat.username or str(chat.id)
        chat_info = f"<b>Cʜᴀᴛ:</b> {chat_title} [<code>{chat.id}</code>]\n"
    
    # Current timestamp
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Select appropriate emoji for log level
    level_emoji = {
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "ERROR": "🚨",
        "SUCCESS": "✅"
    }.get(level.upper(), "📝")
    
    # Format the message
    formatted_message = (
        f"{level_emoji} <b>{level.upper()}</b> {level_emoji}\n\n"
        f"<b>Tɪᴍᴇsᴛᴀᴍᴘ:</b> <code>{current_date}</code>\n"
        f"<b>Usᴇʀ:</b> {user_mention}\n"
        f"{chat_info}"
        f"<b>Mᴇssᴀɢᴇ:</b>\n\n{msg}"
    )
    
    # Handle long messages
    if len(formatted_message) > 4000:
        # Truncate message if too long
        formatted_message = formatted_message[:3950] + "...\n<i>[Message truncated due to length]</i>"
    
    try:
        # Send the message
        await context.bot.send_message(
            chat_id=LOGGER_CHATID, 
            text=formatted_message, 
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True  # Prevent URLs from expanding
        )
        return True
    except Exception as e:
        # If sending fails, return False
        print(f"Failed to send log message: {e}")
        return False


async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Helper function to log when admin commands are used.
    Captures the command and its arguments.
    """
    if not update.effective_message or not update.effective_message.text:
        return
    
    command_text = update.effective_message.text
    
    # Format: "Command: /something arg1 arg2" with args bolded
    command_parts = command_text.split()
    if len(command_parts) > 1:
        command = command_parts[0]
        args = ' '.join(command_parts[1:])
        msg = f"<b>Command:</b> <code>{command}</code>\n<b>Arguments:</b> <code>{args}</code>"
    else:
        msg = f"<b>Command:</b> <code>{command_text}</code>"
    
    await LOG(update, context, msg)