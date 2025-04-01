import html
import json
import traceback
from typing import Any, Dict, Optional, Union

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import (BadRequest, Conflict, NetworkError, RetryAfter,
                            TelegramError)
from telegram.ext import ContextTypes

from config import DEBUG_MODE, LOGGER_CHATID
from utils.log import logger


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Log the error and send a telegram message to notify the developer.

    Handles common Telegram API errors specially and provides more context
    about the error for easier debugging.
    """
    # Extract error information
    error = context.error

    # Log the error with appropriate level based on error type
    if isinstance(error, Conflict):
        logger.warning(f"Conflict error occurred: {error}")
        # For conflict errors, we might not want to notify developers each time
        if not DEBUG_MODE:
            return
    elif isinstance(error, RetryAfter):
        logger.warning(f"Rate limit hit. Retry after {error.retry_after} seconds")
    elif isinstance(error, NetworkError):
        logger.error(f"Network error occurred: {error}")
    elif isinstance(error, BadRequest):
        logger.warning(f"Bad request: {error}")
    else:
        logger.error("Exception while handling an update:", exc_info=error)

    # Format traceback information
    tb_list = traceback.format_exception(None, error, error.__traceback__)
    tb_string = "".join(tb_list)

    # Get update information safely
    update_info = _get_update_info(update)

    # Build message with better formatting and more relevant information
    message = _format_error_message(update_info, context, tb_string, error)

    # Handle message size limit (Telegram has a 4096 character limit)
    messages = _split_message_if_needed(message)

    # Send notification to developers
    try:
        for msg in messages:
            await context.bot.send_message(
                chat_id=LOGGER_CHATID, text=msg, parse_mode=ParseMode.HTML
            )
    except Exception as send_error:
        # If we can't send the error message, log it locally
        logger.critical(
            f"Failed to send error notification: {send_error}\nOriginal error: {error}"
        )


def _get_update_info(update: object) -> Dict[str, Any]:
    """Safely extract information from the update object."""
    if isinstance(update, Update):
        # For regular Update objects, let's extract the most relevant info
        update_info = {}

        # Add message info if available
        if update.effective_message:
            update_info["message"] = {
                "message_id": update.effective_message.message_id,
                "chat": {
                    "id": update.effective_message.chat.id,
                    "type": update.effective_message.chat.type,
                    "title": getattr(update.effective_message.chat, "title", None),
                },
                "text": (
                    update.effective_message.text
                    if hasattr(update.effective_message, "text")
                    else "[No text]"
                ),
                "from": (
                    {
                        "id": (
                            update.effective_message.from_user.id
                            if update.effective_message.from_user
                            else None
                        ),
                        "username": (
                            update.effective_message.from_user.username
                            if update.effective_message.from_user
                            else None
                        ),
                    }
                    if update.effective_message.from_user
                    else None
                ),
            }

        # Add callback query info if available
        if update.callback_query:
            update_info["callback_query"] = {
                "id": update.callback_query.id,
                "data": update.callback_query.data,
                "from_user": {
                    "id": update.callback_query.from_user.id,
                    "username": update.callback_query.from_user.username,
                },
            }

        return update_info
    else:
        # For non-Update objects, convert to string with some basic sanitation
        try:
            return {"raw_update": str(update)[:1000]}  # Limit to 1000 chars
        except:
            return {"raw_update": "Unable to convert update to string"}


def _format_error_message(
    update_info: Dict[str, Any],
    context: ContextTypes.DEFAULT_TYPE,
    tb_string: str,
    error: Exception,
) -> str:
    """Format the error message with clear sections and better HTML formatting."""
    # Get error type for the header
    error_type = error.__class__.__name__

    # Format the message with sections
    sections = [
        f"<b>🚨 ERROR: {html.escape(error_type)}</b>",
        f"<b>Message:</b> <code>{html.escape(str(error)[:500])}</code>",
        "",
        "<b>📋 UPDATE INFO:</b>",
        f"<pre>{html.escape(json.dumps(update_info, indent=2, ensure_ascii=False))}</pre>",
        "",
    ]

    # Only include user and chat data if they exist and aren't empty
    if context.user_data and len(context.user_data) > 0:
        sections.extend(
            [
                "<b>👤 USER DATA:</b>",
                f"<pre>{html.escape(str(context.user_data)[:1000])}</pre>",
                "",
            ]
        )

    if context.chat_data and len(context.chat_data) > 0:
        sections.extend(
            [
                "<b>💬 CHAT DATA:</b>",
                f"<pre>{html.escape(str(context.chat_data)[:1000])}</pre>",
                "",
            ]
        )

    # Add traceback at the end (usually the longest part)
    sections.extend(["<b>🔍 TRACEBACK:</b>", f"<pre>{html.escape(tb_string)}</pre>"])

    return "\n".join(sections)


def _split_message_if_needed(message: str) -> list[str]:
    """Split message if it exceeds Telegram's message size limit."""
    MAX_MESSAGE_LENGTH = 4000  # Slightly less than Telegram's 4096 to be safe

    if len(message) <= MAX_MESSAGE_LENGTH:
        return [message]

    messages = []
    current_message = []
    current_length = 0

    # Split by lines to avoid breaking HTML tags
    for line in message.split("\n"):
        line_length = len(line) + 1  # +1 for the newline

        if current_length + line_length > MAX_MESSAGE_LENGTH:
            # Current message would exceed limit, finalize it
            messages.append("\n".join(current_message))
            current_message = []
            current_length = 0

        # Add this line to the current message
        current_message.append(line)
        current_length += line_length

    # Add the last message if there's anything left
    if current_message:
        messages.append("\n".join(current_message))

    # Add part numbers for clarity
    for i in range(len(messages)):
        if i == 0:
            messages[i] = (
                f"<b>Error Report (Part {i+1}/{len(messages)})</b>\n\n" + messages[i]
            )
        else:
            messages[i] = (
                f"<b>Error Report (Part {i+1}/{len(messages)}) - Continued</b>\n\n"
                + messages[i]
            )

    return messages
