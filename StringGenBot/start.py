from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from env import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""اهلا {msg.from_user.mention},

انا {me2},


صنع من قبل سورس الساحر : [Alsaher](tg://user?id={OWNER_ID}) !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="استخراج جلسه", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("سورس الساحر", url="https://t.me/SXYO3"),
                    InlineKeyboardButton("المطور", user_id=OWNER_ID)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
    
print ("حقوق الساحر🤙🏻🤙🏻")
