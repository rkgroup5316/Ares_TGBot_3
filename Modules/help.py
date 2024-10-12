from utils.log import logger
from Modules.inline import *
from assets.assets import load_asset
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
)
from config import * # imports all the attributes and modules
from utils.decoders_ import rate_limit
from utils.dataBase.FireDB import DB

LIST_OF_BAN_IDS = DB.blocked_users_cache




async def get_explanation(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str):
    keyboard = [
        [InlineKeyboardButton("⬅ Back", callback_data=f"back_{command.split('_')[0]}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    command_title = command.replace("_", " ").title()  # Convert to Pascal case
    formatted_text = f"<b>{command_title}</b>\n\n{INFO_help.get(command, 'No information available for this command.')}"
    if len(formatted_text) > 1024:
        keyboard = [
        [InlineKeyboardButton("❌ᴄʟᴏsᴇ", callback_data="close")],
    ]   
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id ,text=formatted_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        if update.callback_query.message.photo:
            try:
                await update.callback_query.edit_message_caption(formatted_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
                return
            except Exception as e:
                logger.error(f"An error occure while getting explanition of inline and sendit as caption error:{e}")
                    
       
        keyboard = [
                [InlineKeyboardButton("❌ᴄʟᴏsᴇ", callback_data="close")],
        ]   
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(formatted_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML )
       

# Function to handle the initial home command
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # if DB.is_user_blocked(str(update.message.from_user.id)):
    #     logger.info(f"Ignoring command from blocked user {str(update.message.from_user.id)}.")
    #     keyboard = [
    #     [InlineKeyboardButton("❌ᴄʟᴏsᴇ", callback_data="close")],
    #         ]   
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #     context.bot.send_message(chat_id=update.effective_chat.id ,text="Yᴏᴜ ᴀʀᴇ ʙᴇᴇɴ 🚫ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ. ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴏᴡɴᴇʀ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏ🧐.", reply_markup=reply_markup, parse_mode=ParseMode.HTML )
        
        # return
    keyboard = [
        [InlineKeyboardButton("🛠️ᴄᴏᴍᴍᴀɴᴅs", callback_data="home_commands")],
        [InlineKeyboardButton("✍ᴘʀᴏᴍᴘᴛɪɴɢ", callback_data="home_prompting")],
        [InlineKeyboardButton("📝ᴇxᴛʀᴀ ɪɴғᴏ", callback_data="home_extra_info")],
        [InlineKeyboardButton("💲sᴜᴘᴘᴏʀᴛ", callback_data="home_support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = """👋 Wᴇʟᴄᴏᴍᴇ ᴛᴏ Aʀᴇs! Yᴏᴜʀ ᴀʟʟ-ɪɴ-ᴏɴᴇ ᴅɪɢɪᴛᴀʟ ᴀssɪsᴛᴀɴᴛ ʀᴇᴀᴅʏ ᴛᴏ ᴍᴀᴋᴇ ʏᴏᴜʀ ʟɪғᴇ ᴇᴀsɪᴇʀ.\n Wɪᴛʜ ᴘᴏᴡᴇʀғᴜʟ AI ᴄᴀᴘᴀʙɪʟɪᴛɪᴇs, Aʀᴇs ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴡɪᴛʜ ᴛᴀsᴋs, ᴘʀᴏᴠɪᴅᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ, ᴀɴᴅ ᴇᴠᴇɴ ᴇɴɢᴀɢᴇ ɪɴ ғʀɪᴇɴᴅʟʏ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴ.\n Lᴇᴛ's ɢᴇᴛ sᴛᴀʀᴛᴇᴅ ᴏɴ ᴍᴀᴋɪɴɢ ʏᴏᴜʀ ᴅɪɢɪᴛᴀʟ ᴇxᴘᴇʀɪᴇɴᴄᴇ sᴍᴀʀᴛᴇʀ ᴀɴᴅ ᴍᴏʀᴇ ᴇғғɪᴄɪᴇɴᴛ! 🚀 \n\n <b>ᴘɪᴄᴋ ᴛʜᴇ ᴛᴏᴘɪᴄ ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ɴᴇᴇᴅ ʜᴇʟᴘ:- </b>"""
    photo = load_asset(START_IMAGE_PATH)
    await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML)
    

async def _home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🛠️ᴄᴏᴍᴍᴀɴᴅs", callback_data="home_commands")],
        [InlineKeyboardButton("✍ᴘʀᴏᴍᴘᴛɪɴɢ", callback_data="home_prompting")],
        [InlineKeyboardButton("📝ᴇxᴛʀᴀ ɪɴғᴏ", callback_data="home_extra_info")],
        [InlineKeyboardButton("💲sᴜᴘᴘᴏʀᴛ", callback_data="home_support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = """👋 Wᴇʟᴄᴏᴍᴇ ᴛᴏ Aʀᴇs! Yᴏᴜʀ ᴀʟʟ-ɪɴ-ᴏɴᴇ ᴅɪɢɪᴛᴀʟ ᴀssɪsᴛᴀɴᴛ ʀᴇᴀᴅʏ ᴛᴏ ᴍᴀᴋᴇ ʏᴏᴜʀ ʟɪғᴇ ᴇᴀsɪᴇʀ.\n Wɪᴛʜ ᴘᴏᴡᴇʀғᴜʟ AI ᴄᴀᴘᴀʙɪʟɪᴛɪᴇs, Aʀᴇs ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴡɪᴛʜ ᴛᴀsᴋs, ᴘʀᴏᴠɪᴅᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ, ᴀɴᴅ ᴇᴠᴇɴ ᴇɴɢᴀɢᴇ ɪɴ ғʀɪᴇɴᴅʟʏ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴ.\n Lᴇᴛ's ɢᴇᴛ sᴛᴀʀᴛᴇᴅ ᴏɴ ᴍᴀᴋɪɴɢ ʏᴏᴜʀ ᴅɪɢɪᴛᴀʟ ᴇxᴘᴇʀɪᴇɴᴄᴇ sᴍᴀʀᴛᴇʀ ᴀɴᴅ ᴍᴏʀᴇ ᴇғғɪᴄɪᴇɴᴛ! 🚀 \n\n <b>ᴘɪᴄᴋ ᴛʜᴇ ᴛᴏᴘɪᴄ ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ɴᴇᴇᴅ ʜᴇʟᴘ:- </b>"""
    await update.callback_query.edit_message_caption(text, reply_markup=reply_markup,parse_mode=ParseMode.HTML)


async def handle_home_command(update: Update, context: ContextTypes.DEFAULT_TYPE, query_data: str):
    if query_data == "home_commands":
        await commands(update, context)
    elif query_data == "home_prompting":
        await prompting(update, context)
    elif query_data == "home_extra_info":
        await extra_info(update, context)
    elif query_data == "home_support":
        await handle_support(update, context)

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if callback query is None, use update.message instead
    if update.callback_query:
        query_data = update.callback_query.data
    elif update.message:
        # Extract callback data from the text of the message
        query_data = update.message.text.split(":")[-1].strip()

    # Default to home menu if unable to determine previous menu
    previous_menu = _home

    if query_data == "back_command":
        previous_menu = commands
    elif query_data == "back_prompting":
        previous_menu = prompting
    elif query_data == "back_extra":
        previous_menu = extra_info

    # Display the previous menu
    await previous_menu(update, context)


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [InlineKeyboardButton("👮‍♂️ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅ", callback_data="command_admin_command")],
    [InlineKeyboardButton("🤖ᴀɪ ᴄᴏᴍᴍᴀɴᴅ", callback_data="command_ai_command")],
    [InlineKeyboardButton("🔍sᴇᴀʀᴄʜɪɴɢ ᴄᴏᴍᴍᴀɴᴅ", callback_data="command_searching_command")],
    [InlineKeyboardButton("⚙️sᴇᴛᴛɪɴɢ ᴄᴏᴍᴍᴀɴᴅ", callback_data="command_setting_command")],
    [InlineKeyboardButton("🛠️ᴜᴛɪʟɪᴛʏ ᴄᴏᴍᴍᴀɴᴅ", callback_data="command_utility_command")],
    [InlineKeyboardButton("❓Who are admin?", callback_data="command_who_are_admin")],
    [InlineKeyboardButton("❓what is command limit rate?", callback_data="Command_limit_rate")],
    [InlineKeyboardButton("← ʙᴀᴄᴋ", callback_data="back")],
]

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = """<i>Cᴏᴍᴍᴀɴᴅs ɪɴ Tᴇʟᴇɢʀᴀᴍ ᴀʀᴇ sʜᴏʀᴛᴄᴜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ sᴘᴇᴄɪғɪᴄ ᴀᴄᴛɪᴏɴs ᴏʀ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴏ̨ᴜɪᴄᴋʟʏ. Tʜᴇʏ sᴛᴀʀᴛ ᴡɪᴛʜ ᴀ '/' ғᴏʟʟᴏᴡᴇᴅ ʙʏ ᴀ ᴋᴇʏᴡᴏʀᴅ.\n Aʀɢᴜᴍᴇɴᴛs ᴄᴀɴ ʙᴇ ɢɪᴠᴇɴ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴄᴜsᴛᴏᴍɪᴢᴇ ɪᴛs ʙᴇʜᴀᴠɪᴏʀ.\n Fᴏʀ ᴇxᴀᴍᴘʟᴇ, "<code>/wiki New York</code>" ғᴇᴛᴄʜᴇs ᴛʜᴇ ɪɴғᴏ ғᴏʀ Nᴇᴡ Yᴏʀᴋ.</i>\n\n <b>Cʜᴏᴏsᴇ ᴡʜɪᴄʜ ᴛʏᴘᴇ ᴏғ ᴄᴏᴍᴍᴀɴᴅs:-</b>"""
    await update.callback_query.edit_message_caption(text, reply_markup=reply_markup,parse_mode=ParseMode.HTML)


async def prompting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [InlineKeyboardButton("📜ɪɴᴛʀᴏᴅᴜᴄᴛɪᴏɴ", callback_data="prompting_what")],
    [InlineKeyboardButton("📂ᴍᴇᴅɪᴀ ᴘʀᴏᴍᴘᴛɪɴɢ", callback_data="prompting_media_prompting")],
    [InlineKeyboardButton("💡sᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛ", callback_data="prompting_supported_format")],
    [InlineKeyboardButton("← ʙᴀᴄᴋ", callback_data="back")]
]

    text = """<b>Introduction to prompt design</b> 
<i>Prompt design is the process of creating prompts that elicit the desired response from language models.
Writing well structured prompts is an essential part of ensuring accurate, high quality responses from a language model. 
This page introduces some basic concepts, strategies, and best practices to get you started in designing prompts.</i>\n\n<b>Choose any sub-topic in prompting:-</b>"""
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_caption(text, reply_markup=reply_markup,parse_mode=ParseMode.HTML)


async def extra_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [InlineKeyboardButton("💻ᴅᴇᴠᴇʟᴏᴘᴇʀ", callback_data="extra_info_developer")],
    [InlineKeyboardButton("🐛ʙᴜɢ/ᴠᴇʀsɪᴏɴ", callback_data="extra_info_bug_version")],
    [InlineKeyboardButton("🤝ᴄᴏɴᴛʀɪʙᴜᴛᴇ", callback_data="extra_info_contribute")],
    [InlineKeyboardButton("💬sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", callback_data="extra_info_support_chat")],
    [InlineKeyboardButton("🤔ʜᴏᴡ ᴛᴏ ᴜsᴇ ɪɴ ɢʀᴏᴜᴘ?", callback_data="extra_info_how_to_use_in_group")],
    [InlineKeyboardButton("← ʙᴀᴄᴋ", callback_data="back")]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_caption("Choose an info type:", reply_markup=reply_markup)

async def handle_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⬅ Back", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = """
<b>Support:</b>
You can support me with a small donation 💵 or a cup of coffee ☕ on <a href="https://www.buymeacoffee.com/Rkgroup">Buy Me a Coffee</a>.

<b>Telegram Account:</b> <a href="https://t.me/Rkgroup5316">@Rkgroup5316</a>
<b>Support Chat:</b> Join our official support group on <a href="https://t.me/AresChatBotAi">Telegram</a>.
<b>GitHub:</b> Check out our projects on <a href="https://github.com/RKgroupkg">GitHub</a>.


"""

    await update.callback_query.edit_message_caption(text, reply_markup=reply_markup,parse_mode=ParseMode.HTML)

    
@rate_limit
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    if user_id in LIST_OF_BAN_IDS:
        Username = update.effective_user.first_name
        asset = load_asset(ACCESS_DENIED)
        msg = f"""
⛔ Attention {Username}!

Unfortunately, you have been banned from using this bot by the administrators.

If you have any questions or wish to appeal, please reach out to us.

Thank you."""
        await update.effective_message.reply_photo(photo=asset,caption=msg,reply_markup=START_INLINE_CMD_INGP,parse_mode=ParseMode.HTML)
        return
    

    if update.effective_chat.type == "private":
        await home(update,context)
        
    else:
        msg = f"I ᴘʀᴇғᴇʀ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ <b>ɢʀᴏᴜᴘ</b>."
        asset = load_asset(START_IMAGE_PATH_)
        await update.effective_message.reply_photo(photo=asset,caption=msg,reply_markup=START_INLINE_CMD_INGP,parse_mode=ParseMode.HTML)


