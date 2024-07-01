import os
import time
import shutil 
import psutil
from datetime import datetime 
from utils.log import logger
from PIL import Image, ImageDraw, ImageFont
from assets.assets import load_asset
from speedtest import Speedtest
from Modules.inline import CLOSE_BUTTON
from utils.dataBase.FireDB import DB

from config import BotStartTime
from utils.helper.functions import get_readable_time,get_readable_bytes
from utils.decoders_ import IsAdmin

from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)


@IsAdmin
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image = Image.open('assets/statsbg.jpg').convert('RGB')
    IronFont = ImageFont.truetype("assets\IronFont.otf", 42)
    draw = ImageDraw.Draw(image)
    
    def draw_progressbar(coordinate, progress):
        try:
            # Calculate the end of the progress bar
            progress = 110+ (progress*10.8)
            
            draw.ellipse((105, coordinate-25, 127 , coordinate), fill='#FFFFFF')    
            draw.rectangle((120, coordinate-25, progress, coordinate), fill='#FFFFFF')	
            draw.ellipse((progress-7, coordinate-25, progress+15, coordinate), fill='#FFFFFF')
    
        except Exception as e:
            logger.error(f"An Error occured while drawing stats progress bar error:{e}")
    
    total, used, free = shutil.disk_usage(".")
    process = psutil.Process(os.getpid())
	
    
    botuptime = get_readable_time(time.time() - BotStartTime)
    osuptime  =  get_readable_time(time.time() - psutil.boot_time())
    botusage = f"{round(process.memory_info()[0]/1024 ** 2)} MiB"

    upload= get_readable_bytes(psutil.net_io_counters().bytes_sent)
    download= get_readable_bytes(psutil.net_io_counters().bytes_recv) 
      
    cpu_percentage = psutil.cpu_percent()
    cpu_count = psutil.cpu_count()
    
    ram_percentage = psutil.virtual_memory().percent
    ram_total = get_readable_bytes(psutil.virtual_memory().total)
    ram_used = get_readable_bytes(psutil.virtual_memory().used)	
    
    disk_percenatge = psutil.disk_usage("/").percent
    disk_total = get_readable_bytes(total)
    disk_used = get_readable_bytes(used)
    disk_free = get_readable_bytes(free)
    
    caption = f"<b>OS Uptime:</b> {osuptime}\n<b>Bot Usage:</b> {botusage}\n\n<b>Total Space:</b> {disk_total}\n<b>Free Space:</b> {disk_free}\n\n<b>Download:</b> {download}\n<b>Upload:</b> {upload}"
     
    start = datetime.now()
    msg = await update.message.reply_photo(photo=load_asset(r"Ares_TGBot_3\assets\progress.jpg"),caption=caption,parse_mode="HTML")    
    end = datetime.now()

    draw_progressbar(243, int(cpu_percentage))
    draw.text((225,153), f"( {cpu_count} core, {cpu_percentage}% )", (255, 255, 255), font=IronFont)	

    draw_progressbar(395, int(disk_percenatge))
    draw.text((335,302), f"( {disk_used} / {disk_total}, {disk_percenatge}% )", (255, 255, 255), font=IronFont)
                  
    draw_progressbar(533, int(ram_percentage))
    draw.text((225,445), f"( {ram_used} / {ram_total}, {ram_percentage}% )", (255, 255, 255), font=IronFont)
    
    draw.text((335,600), f"{botuptime}", (255, 255, 255), font=IronFont)
    draw.text((857,607), f"{(end-start).microseconds/1000} ms", (255, 255, 255), font=IronFont)
    
    image.save("stats.png")
    await msg.delete()
    await update.message.reply_photo(photo=load_asset("stats.png"),caption=caption,reply_markup=CLOSE_BUTTON,parse_mode="HTML")
    os.remove("stats.png")



def speedtestcli():
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    return test.results.dict()

@IsAdmin
async def Speed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Give speedtest of the server where bot is running.
    """
    speed = await update.message.reply_text("Running speedtest....")

    logger.info("Running speedtest....")
    result = speedtestcli()
    speed_string = f"""
Upload: {get_readable_bytes(result["upload"] / 8)}/s
Download: {get_readable_bytes(result["download"] / 8)}/s
Ping: {result["ping"]} ms
ISP: {result["client"]["isp"]}
"""
    await speed.delete()
    await update.message.reply_photo(
        photo=result["share"], caption=speed_string,reply_markup=CLOSE_BUTTON)
    

@IsAdmin
async def dbstats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Returns database stats of firebase, which includes Total number
    of bot user and total number of bot chats.
    """ 
    TOTALCHAT = DB.get_usernames()
    TOTAL_BLOCKED_USERS =DB.blocked_users_cache
    TOTAL_ADMINS = DB.admins_users

    stats_string = f"<b>Bot Database Statics.\n\n</b><b>Total Number of users:</b> <i>{len(TOTALCHAT)}</i>\n<b>Blocked users: </b><i>{len(TOTAL_BLOCKED_USERS)}</i>\n<b>Total Number of Admins :</b><i>{len(TOTAL_ADMINS)}</i>"
    await update.message.reply_text(stats_string,parse_mode="HTML",reply_markup=CLOSE_BUTTON)


@IsAdmin
async def LOG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    upload the logs file of the bot.
    """

    try:
        await update.message.reply_document(open("logs.txt","rb"), caption="logs.txt",reply_markup=CLOSE_BUTTON)
    except Exception as error:
       await update.message.reply_text(f"An error occured while getting log file{error}",reply_markup=CLOSE_BUTTON)

STATS_CMD = CommandHandler(("stats","health","hh"),stats)
SPEED_CMD = CommandHandler(("speed","speedtest","net_speed"),Speed)
DBSTATS = CommandHandler(("dbstats","data_base_stats","dataBaseStats","dataBase_stats"),dbstats)
LOG_CMD = CommandHandler(("log","logs"),LOG)
