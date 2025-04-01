from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import BOTS_USERNAME, OWNER_USERNAME

START_INLINE_CMD = [
    [
        InlineKeyboardButton(text="📚 ʜᴇʟᴘ ᴀɴᴅ ɪɴғᴏ", callback_data="help"),
    ],
    [
        InlineKeyboardButton(
            text="🧑‍💻ᴅᴇᴠʟᴏᴘᴇʀ",
            url=f"https://t.me/{OWNER_USERNAME}",
        ),
    ],
    [
        InlineKeyboardButton(
            text="Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Gʀᴏᴜᴘ",
            url=f"https://t.me/{BOTS_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="❌ᴄʟᴏsᴇ​", callback_data="close"),
    ],
]

START_INLINE_CMD = InlineKeyboardMarkup(START_INLINE_CMD)

START_INLINE_CMD_INGP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="👤 ᴏᴩᴇɴ ɪɴ ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ",
                url=f"https://t.me/{BOTS_USERNAME}?start=help",
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 ᴏᴩᴇɴ ʜᴇʀᴇ",
                callback_data="help",
            )
        ],
    ]
)

RATE_LIMITION = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("❌ᴄʟᴏsᴇ", callback_data="close")],
        [
            InlineKeyboardButton(
                "what is command rate limit ❓", callback_data="Command_limit_rate"
            )
        ],
    ]
)

ADMIN_ERROR = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("❌ᴄʟᴏsᴇ", callback_data="close")],
        [
            InlineKeyboardButton(
                "Who are admin❓", callback_data="command_who_are_admin"
            )
        ],
    ]
)

CLOSE_BUTTON = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("❌ᴄʟᴏsᴇ", callback_data="close")],
    ]
)

music_limit_error = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("❌ᴄʟᴏsᴇ", callback_data="close")],
        [
            InlineKeyboardButton(
                "What is this Error❓", callback_data="command_music_limit_error"
            )
        ],
    ]
)
