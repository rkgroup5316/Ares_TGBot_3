from utils.log import logger

import asyncio
import sys
import html
import traceback
from io import  StringIO
from os import remove

from utils.decoders_ import IsOwner

from utils.helper.pasting_servises import katbin_paste
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)


@IsOwner
async def Shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Executes command in terminal via bot.
    """
    args = context.args
    if not args:
        shell_usage = f"<b>USAGE:</b> Executes terminal commands directly via bot.\n\n<b>Example: </b><pre>/shell pip install requests</pre>"
        await update.message.reply_text(shell_usage,parse_mode="HTML")
        return
    
    content = ' '.join(args)


    try:
        shell_replymsg = await update.message.reply_text("running...")
        shell = await asyncio.create_subprocess_exec(content, stdout=-1, stderr=-1)
        stdout, stderr = await shell.communicate()
        result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    except Exception as error:

        if len(error) > 3980:
            logger.error(f"{error}")
            await shell_replymsg.edit_text("error output too large. sending it as a file pasting it..")
            output = await katbin_paste(error)
            keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Open in Browser", url=output)]
                ])
            return await shell_replymsg.edit_text(f"Error :- {html.escape(output)}",reply_markup=keyboard)
        else:
            return await shell_replymsg.edit_text(f"Error :-\n\n{error}")


        
        
    
    if len(result) > 4000:
        await shell_replymsg.edit_text("output too large. sending it as a file pasting it..")
        output = await katbin_paste(result)
        keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Open in Browser", url=output)]
            ])
        await shell_replymsg.edit_text(f"output too large.\n\nSee the output at:{output}",reply_markup=keyboard)
    else:
        await shell_replymsg.edit_text(f"<b>Output :-</b>\n\n<pre>{html.escape(result)}</pre>",parse_mode="HTML")




@IsOwner
async def Python(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        Python_usage =f"<b>Usage:</b> Executes python commands directly via bot.\n\n<b>Example: </b><pre>/exec print('hello world')</pre>"
        await update.message.reply_text(Python_usage,parse_mode="HTML")
        return
    
    

    replymsg = await update.message.reply_text("executing..", quote=True)
    await py_runexec(update, context, replymsg)



async def aexec(code,update: Update, context: ContextTypes.DEFAULT_TYPE):
    exec(
        "async def __aexec(update, context): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](update, context)

async def py_runexec(update: Update, context: ContextTypes.DEFAULT_TYPE, replymsg):
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None

    args = context.args
    code =' '.join(args)

    try:
        await aexec(code, update, context)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""         
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "success"
    final_output = f"{evaluation.strip()}"

    
    try:
        if len(final_output) > 4000:
            await replymsg.edit_text("output too large. sending it as a file pasting it..")
            output = await katbin_paste(final_output)
            keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Open in Browser", url=output)]
                ])
            await replymsg.edit_text(f"output too large.\n\nSee the output at:{output}",reply_markup=keyboard)
        else:
            await replymsg.edit_text(f"<b>Output :-</b>\n\n<pre>{html.escape(final_output)}</pre>",parse_mode="HTML")
    except Exception as e:
        logger.warning("retrying wth /paste feature")
        await replymsg.edit_text("An error occured while sending. sending it as a file pasting it..")
        output = await katbin_paste(final_output)
        keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Open in Browser", url=output)]
                ])
        await replymsg.edit_text(f"output too large.\n\nSee the output at:{output}",reply_markup=keyboard)





SHELL_CMD = CommandHandler(("power_shell","shell","ps"),Shell)
EXECUTE_COMMAND = CommandHandler(("py","python","execute"),Python)