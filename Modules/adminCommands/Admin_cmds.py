import html

import telegram
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from utils.dataBase.FireDB import DB
from utils.decoders_ import IsAdmin
from utils.Group_log import LOG

LIST_OF_BAN_IDS = DB.blocked_users_cache
LIST_ADMIN_USER_IDS = DB.admins_users


@IsAdmin
async def Chat_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Give sback user info to the admin who asked that

    """

    UsersId = context.args

    if not UsersId:
        await update.message.reply_text("Usᴀɢᴇ: /chat_info (ᴄʜᴀᴛ_ɪᴅ)")
        return

    if len(UsersId) > 30:
        await update.message.reply_text(
            "Maximum of 30 users can be only shown in one time.\n\nUsᴀɢᴇ: /chat_info (ᴄʜᴀᴛ_ɪᴅ)"
        )
        return

    msg = await update.message.reply_html("<b>Extracting info...</b>")

    for chat_id_str in UsersId:
        try:
            chat_id = int(chat_id_str)

            # Get chat information and format response
            try:
                chat = await context.bot.get_chat(chat_id)
                chat_data = {
                    "➻ cʜᴀᴛ ɪᴅ": f"<code>{chat.id}</code>",
                    "➻ cʜᴀᴛ ᴛʏᴘᴇ": chat.type,
                    "➻ ᴛɪᴛʟᴇ": chat.title,
                    "➻ ᴜsᴇʀɴᴀᴍᴇ": chat.username,
                    "➻ ғɪʀsᴛ ɴᴀᴍᴇ": chat.first_name,
                    "➻ ʟᴀsᴛ ɴᴀᴍᴇ": chat.last_name,
                    "➻ ᴘʜᴏᴛᴏ": chat.photo,
                    "➻ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ": chat.description,
                    "➻ ɪɴᴠɪᴛᴇ ʟɪɴᴋ": chat.invite_link,
                    "➻ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ": (
                        chat.pinned_message.text if chat.pinned_message else None
                    ),
                    "➻ sᴛɪᴄᴋᴇʀ sᴇᴛ ɴᴀᴍᴇ": chat.sticker_set_name,
                    "➻ ᴄᴀɴ sᴇᴛ sᴛɪᴄᴋᴇʀ sᴇᴛ": chat.can_set_sticker_set,
                    "➻ ʟɪɴᴋᴇᴅ ᴄʜᴀᴛ ɪᴅ": chat.linked_chat_id,
                    "➻ ʟᴏᴄᴀᴛɪᴏɴ": chat.location,
                    "➻ ᴊᴏɪɴ ʙʏ ʀᴇǫᴜᴇsᴛ": chat.join_by_request,
                    "➻ ᴘᴇʀᴍɪssɪᴏɴs\n\n": chat.permissions,
                }
                filtered_data = {k: v for k, v in chat_data.items() if v is not None}
                info_text = "\n".join(
                    [f"{key}: {value}" for key, value in filtered_data.items()]
                )
                # Send response for each chat
                await msg.edit_text(
                    f"Cʜᴀᴛ Iɴғᴏʀᴍᴀᴛɪᴏɴ:\n{info_text}", parse_mode="HTML"
                )
            except telegram.error.Forbidden:
                await msg.edit_text(
                    f"Cʜᴀᴛ ID {chat_id}: I ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴛʜɪs ᴄʜᴀᴛ."
                )
            except telegram.error.BadRequest as e:
                await msg.edit_text(
                    f"Cʜᴀᴛ ID {chat_id}: Bᴀᴅ ʀᴇᴏ̨ᴜᴇsᴛ. Eʀʀᴏʀ: {e.message}"
                )
            except Exception as e:
                await msg.edit_text(
                    f"Cʜᴀᴛ ID {chat_id}: Fᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴄʜᴀᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ. Eʀʀᴏʀ: {e}"
                )
        except ValueError:
            await msg.edit_text(
                f"Iɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ID: {chat_id_str}. Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ɴᴜᴍᴇʀɪᴄ ᴄʜᴀᴛ IDs."
            )


@IsAdmin
async def Chat_Data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gives data from the user bots usage

    """
    UsersId = context.args
    if not UsersId:
        await update.message.reply_text("Usᴀɢᴇ: /user_data (ᴄʜᴀᴛ_ɪᴅ)")
        return

    msg = await update.message.reply_html("<b>Extracting info ...</b>")
    userId = UsersId[0]

    chat = await context.bot.get_chat(userId)
    if chat.type == "private":
        first_name = chat.first_name
    else:
        first_name = chat.title

    if userId in LIST_OF_BAN_IDS:
        is_banned = "Yes"
    else:
        is_banned = "No"

    ai_prompt = DB.extract_instruction(userId)

    User_data = DB.user_exists(userId)
    if User_data:
        used_ai = "Yes"
    else:
        used_ai = "No"

    if userId in LIST_ADMIN_USER_IDS:
        user_admin = "Yes"
    else:
        user_admin = "No"

    Info = f"""
<b>» Chat data:- </b>

➻ ᴜsᴇʀɴᴀᴍᴇ: <a href='tg://user?id={chat.id}'>{first_name}</a>
➻ ɪs ʙᴀɴɴᴇᴅ:  {is_banned}
➻ Is ᴀᴅᴍɪɴ:   {user_admin}
➻ ᴀɪ ᴘʀᴏᴍᴘᴛ:  {html.escape(ai_prompt)}
➻ ᴜsᴇᴅ ᴀɪ:    {used_ai}
"""
    await msg.edit_text(Info, parse_mode="HTML")


@IsAdmin
async def BAN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    UsersId = context.args
    if not UsersId:
        await update.message.reply_text("Usᴀɢᴇ: /ban (ᴄʜᴀᴛ_ɪᴅ)/(ᴜsᴇʀ_ɪᴅ)")
        return

    msg = await update.message.reply_html("<b>Bᴀɴɴɪɴɢ ᴛʜᴇ ᴜsᴇʀ....</b>")

    added_users_info = ""

    for chat_id_str in UsersId:
        try:
            DB.block_user(chat_id_str)
            try:
                user = await context.bot.get_chat(chat_id_str)
                added_users_info = f"""
<b>User:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>
<b>User ID:</b> {user.id}
"""

            except Exception as e:
                added_users_info += f"\nFᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴜsᴇʀ ɪɴғᴏ ғᴏʀ: {chat_id_str}"
            log = f"""
<b>🔨» User Banned</b>
{added_users_info}
"""
            await LOG(update, context, log)
        except Exception as e:
            await msg.edit_text(f"Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ʙᴀɴɴɪɴɢ ᴛʜᴇ ᴜsᴇʀ: {e}")

    await msg.edit_text("<b>🔨 User Banned Successfully</b>", parse_mode="HTML")


@IsAdmin
async def Un_BAN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    UsersId = context.args
    if not UsersId:
        await update.message.reply_text("Usᴀɢᴇ: /Unban (ᴄʜᴀᴛ_ɪᴅ)/(ᴜsᴇʀ_ɪᴅ")
        return

    msg = await update.message.reply_html("<b>UɴBᴀɴɴɪɴɢ ᴛʜᴇ ᴜsᴇʀ....</b>")

    added_users_info = ""

    for chat_id_str in UsersId:
        try:
            DB.unblock_user(chat_id_str)
            try:
                user = await context.bot.get_chat(chat_id_str)
                added_users_info = f"""
<b>User:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>
<b>User ID:</b> {user.id}
"""
            except Exception as e:
                added_users_info += f"\nFᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴜsᴇʀ ɪɴғᴏ ғᴏʀ: {chat_id_str}"
            log = f"""
<b>🔓» User UɴBanned</b>
{added_users_info}
"""
            await LOG(update, context, log)
        except Exception as e:
            await msg.edit_text(f"Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ Uɴʙᴀɴɴɪɴɢ ᴛʜᴇ ᴜsᴇʀ: {e}")

    await msg.edit_text("<b>🔓 User UɴBanned Successfully</b>", parse_mode="HTML")


CHAT_INFO_CMD = CommandHandler(("cid_info", "chat_info"), Chat_info)
CHAT_DATA_CMD = CommandHandler(("user_data", "chat_data"), Chat_Data)
BAN_CMD = CommandHandler(("ban", "block"), BAN)
UN_BAN_CMD = CommandHandler(("unban", "un_ban", "unblock"), Un_BAN)
