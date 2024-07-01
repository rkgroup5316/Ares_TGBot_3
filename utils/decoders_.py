from functools import wraps
from utils.log import logger
from assets.assets import load_asset
from config import ERROR429,LOGGER_CHATID,OWNER_ID
from utils.dataBase.FireDB import DB
from Modules.inline import ADMIN_ERROR

from Modules.inline import RATE_LIMITION
from utils.rate_limit import RateLimiter
from cachetools import TTLCache


LIST_OF_BAN_IDS = DB.blocked_users_cache
ADMIN_ID_LIST = DB.admins_users

ratelimit = RateLimiter()

# storing spammy user in cache for 1minute before allowing them to use commands again.
warned_users = TTLCache(maxsize=128, ttl=60)
warning_message = "Spam detected! ignoring your all requests for few minutes."
WARNNED_USERS_NOTIFYED =[] 

def rate_limit(func):
    """
    Restricts user's from spamming commands or pressing buttons multiple times
    using leaky bucket algorithm and pyrate_limiter.
    """
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        userid = update.effective_user.id
        is_limited = await ratelimit.acquire(userid)
        

        if is_limited and userid not in warned_users:
            
            await update.message.reply_photo(photo=load_asset(ERROR429),caption=warning_message,reply_markup=RATE_LIMITION)
            warned_users[userid] = 1
            
            return

        elif is_limited and userid in warned_users: 
            message = f"First Name : {update.effective_user.first_name},UserId: <code>{userid}</code>\n\n Has been caught spamming even after message is send."
            await context.bot.send_message(
                chat_id=LOGGER_CHATID, text=message, parse_mode="HTML"
            )
        else: 
            await func(update, context, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper








def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = str(update.effective_user.id)
        if user_id in LIST_OF_BAN_IDS:
            logger.info(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped


def IsAdmin(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = str(update.effective_user.id)
        if  user_id in ADMIN_ID_LIST or  user_id == str(OWNER_ID):

            return await func(update, context, *args, **kwargs)
        else:
            logger.info(f"Unauthorized access denied for {user_id} not in admin list :{ADMIN_ID_LIST}.")
            await update.message.reply_text("Aᴄᴄᴇss ᴅᴇɴɪᴇᴅ. Oɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs.", reply_markup=ADMIN_ERROR)
            return
    return wrapped

def IsOwner(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = str(update.effective_user.id)
        if  user_id == str(OWNER_ID):

            return await func(update, context, *args, **kwargs)
        else:
            logger.info(f"Unauthorized access denied for {user_id} not in admin list :{ADMIN_ID_LIST}.")
            await update.message.reply_text("Aᴄᴄᴇss ᴅᴇɴɪᴇᴅ. Oɴʟʏ Owner ᴄᴀɴ ᴅᴏ ᴛʜɪs.")
            return
    return wrapped

