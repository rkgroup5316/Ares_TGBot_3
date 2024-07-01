
import time
import requests

from utils.log import logger


from telegram.constants import ParseMode,ChatAction
from utils.decoders_ import rate_limit,restricted
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)

def create_image(prompt: str) -> bytes:
        """Generates an AI-generated image based on the provided prompt.

        Args:
            prompt (str): The input prompt for generating the image.

        Returns:
            bytes: The generated image in bytes format.
            
        Example usage:
      
        >>> generated_image= ai_image("boy image")
        >>> print(generated_image)
        """
        url = "https://ai-api.magicstudio.com/api/ai-art-generator"

        form_data = {
            'prompt': prompt,
            'output_format': 'bytes',
            'request_timestamp': str(int(time.time())),
            'user_is_subscribed': 'false',
        }

        response = requests.post(url, data=form_data)
        if response.status_code == 200:
            try:
                if response.content:
                    return response.content
                else:
                    raise Exception("Failed to get image from the server.")
            except Exception as e:
                raise e
        else:
            raise Exception("Error:", response.status_code)

@rate_limit
@restricted
async def IMAGINE(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    search = " ".join(context.args)
    if not search:
        await update.message.reply_text(f"Eʀʀᴏʀ 404 ɴᴏ ᴘʀᴏᴍᴛ ᴘʀᴏᴠɪᴅᴇᴅ ᴘʟs ᴘʀᴏᴠɪᴅᴇ ᴘʀᴏᴍᴘᴛ")
        return 
    start_time = time.time()
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.FIND_LOCATION)
    try:
        seraching_reply = await update.message.reply_text("Generating...")
        logger.info(f"requesting for image for chatId:{chat_id}  prompt:{search}")
        Image_genratred = create_image(search)
        logger.info(f"image created successfully")
        end_time = time.time()
        elapsed_time = end_time - start_time

        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)
        user = update.effective_user
        caption = f"""
✨ᴘʀᴏᴍᴘᴛ: {search}\n
🥀ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ: <a href='tg://user?id={user.id}'>{user.first_name}</a>
⏳ᴛɪᴍᴇ ᴛᴀᴋᴇɴ:{round(elapsed_time,2)} Sec
- ɢᴇɴʀᴀᴛᴇᴅ ʙʏ @ᴀʀᴇs_ᴄʜᴀᴛʙᴏᴛ
"""
        keyboard = [
        [InlineKeyboardButton("❌ᴄʟᴏsᴇ", callback_data="close")],
    ]   
        reply_markup = InlineKeyboardMarkup(keyboard)
        await seraching_reply.delete()
        await update.message.reply_photo(photo=Image_genratred, caption=caption, quote=True,reply_markup=reply_markup,parse_mode=ParseMode.HTML)
    except Exception as e:
        await update.message.reply_text(f"Eʀʀᴏʀ ᴡʜɪʟᴇ ɢᴇɴᴇʀᴀᴛɪɴɢ ɪᴍᴀɢᴇ ᴇʀʀᴏʀ: {e}")
        logger.error(f"error while generating image error : {e}")
        
    


IMAGINE_COMMAND_HANDLLER = CommandHandler(("imagine","genrate_image","create_image"),IMAGINE)