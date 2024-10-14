from telegram.constants import ParseMode,ChatAction
from utils.decoders_ import rate_limit,restricted
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes
)


from utils.log import logger
import yt_dlp

import html
import uuid
import math
import requests
import os

from config import video_urls ,FIXIE_SOCKS_HOST




def beautify_views(views):
    views =''.join(filter(str.isdigit, views))

    views = int(views)
    if views < 1000:
        return str(views)
    elif views < 1_000_000:
        return f"{views / 1000:.1f} <b>k</b>"
    elif views < 1_000_000_000:
        return f"{views / 1_000_000:.1f} <b>m</b>"
    else:
        return f"{views / 1_000_000_000:.1f} <b>b</b>"

@rate_limit
@restricted
async def YOUTUBE_CALL_BACK(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    message_id = query.message.message_id  # Get the ID of the message to delete


    user_name = query.from_user.first_name
    user_id = query.from_user.id
    action, video_uuid = query.data.split(":")
    data = video_urls.get(video_uuid)
    user_info = f"<a href='tg://user?id={str(user_id)}'>{html.escape(user_name)}</a>"

    video_url = f"https://youtube.com{data['url_suffix']}"
    if not video_url:
        await update.callback_query.edit_message_caption("Error: Video URL not found.")
        return
    title = html.escape(data["title"][:40])
    duration = data["duration"]
    views = data["views"]
    channel_name = data.get("channel", "Unknown Channel")
    thumbnail = data["thumbnails"][0]
    thumb_name = f"thumb{str(uuid.uuid4())}.jpg"
    inline_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Watch Video on YouTube", url=video_url)]])

    
    rep = (
                    f"<b>Title:</b>        <i>{title}</i>\n"
                    f"<b>Duration:</b>     <i>{duration}</i>\n"
                    f"<b>Views:</b>        <i>{beautify_views(views)}</i>\n"
                    f"<b>Requested by:</b> {user_info}"
                )
    
    await update.callback_query.edit_message_caption(f"Downloading {action}... \n\n{rep}",parse_mode='HTML')

    try:
            ydl_opts = {
            "format": "bestaudio[ext=m4a]" if action == "audio" else "best[ext=mp4]",
            "outtmpl": "%(title)s.%(ext)s",
            "noplaylist": True,
            "quiet": True,
            "retries": 2,
            "fragment_retries": 3,
            "continuedl": True,
            "nocheckcertificate": True,
            "http_chunk_size": 10485760,
            "proxy": f"socks5://{FIXIE_SOCKS_HOST}",
            "external_downloader_args": ["-x", "20", "-k", "1M"]  # 20 connections, 1MB chunks
        }


            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if action == "audio":
                    info_dict = ydl.extract_info(video_url, download=False)
                    file_name = ydl.prepare_filename(info_dict)
                    ydl.process_info(info_dict)  # Download audio now
                    thumb = requests.get(thumbnail, allow_redirects=True)
                    open(thumb_name, "wb").write(thumb.content)
                else:
                    info_dict = ydl.extract_info(video_url, download=True)
                    file_name = ydl.prepare_filename(info_dict)

    
            
                await context.bot.send_chat_action(chat_id=query.message.chat_id, action="upload_" + ("audio" if action == "audio" else "video"))
                await context.bot.delete_message(chat_id=query.message.chat_id, message_id=message_id)

                with open(file_name, "rb") as file:
                    if action == "audio":
                        
                        with open(thumb_name, "rb") as thumb_file:
                            await context.bot.send_audio(
                                    chat_id=update.effective_chat.id,
                                    audio=file,
                                    thumbnail=thumb_file,
                                    caption=rep,
                                    parse_mode='HTML',
                                    title=title,
                                    performer=channel_name,
                                    reply_markup=inline_keyboard,
                                    duration=int(duration.split(':')[0]) * 60 + int(duration.split(':')[1])  # Convert duration to seconds
                                )
                    else:
                        await context.bot.send_video(chat_id=query.message.chat_id, video=file, caption=rep,parse_mode='HTML',reply_markup=inline_keyboard)

                try:
                    os.remove(file_name)
                except Exception as e:
                    print(f"Error while deleting Audi/video file:{file_name},error:{e}")
                try:
                    if os.path.exists(thumb_name):
                        os.remove(thumb_name)
                except Exception as e:
                    print(f"Error while deleting Thumnail file:{thumb_name},error:{e}")


    except Exception as e:
            await update.callback_query.edit_message_caption(f"Error during download: {str(e)}")
            logger.error(f"Error during download: {str(e)}")
            try:
                    os.remove(file_name)
            except Exception as e:
                    print(f"Error while deleting Audi/video file:{file_name},error:{e}")
            try:
                    if os.path.exists(thumb_name):
                        os.remove(thumb_name)
            except Exception as e:
                    print(f"Error while deleting Thumnail file:{thumb_name},error:{e}")





