from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import env



ask_ques = "**»اختار اي جلسه تريد التنصيب عليها رجائا :**"
buttons_ques = [
    [
        InlineKeyboardButton("pyrogram", callback_data="pyrogram"),
        InlineKeyboardButton("telethon", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("pyro bot", callback_data="pyrogram_bot"),
        InlineKeyboardButton("telethon bot", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="بدء الاستخراج 🪄", callback_data="generate")
    ]
]




@app.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def bot(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "telethon"
    else:
        ty = "pyrogram"
    if is_bot:
        ty += "bot"
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "رجائا ارسل الايبي ايدي الخاص بك  او للتخطي.\n\اضغط على /skip وسوف يتم استعمال ايبي عشوائي.", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = env.API_ID
        api_hash = env.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**الايبي ايدي** لازم يكون بس ارقام.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "»الان رجائا ارسل **الايبي هاش **", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "» ارسل رقم الهاتف مع الرمز الدولي  \nمثلا  : `+910000000000`'"
    else:
        t = "رجائا ارسل **البوت توكن** للاستمرار.\مثال : `5432198765:abcdanonymousterabaaplol`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("» يتم ارسال الكود...")
    else:
        await msg.reply("» يتم تسجيل الدخول في البوت...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("» الايبي ايدي والايبي هاش خاصك خاطئ . \n\رجائا اعد المحاوله", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("»رقم الهاتف الخاص بك خاطئ", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "» ارسل الكود الذي وصل لك \nɪғ الكود يكون بهذا الشكل `12345`, **ارسله بهذا الشكل** `1 2 3 4 5`.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("» خلص وقتك اعد المحاوله.\n\او تواصل مع المطور بحال وجود خطأ", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("» الكود يلي دزيته غلط مو كتلك بهذا الشكل 1 2 3 4 5", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("» الكود يلي دزيته خلص وقته او يمكن دزيته بشكل خاطئ", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, "» الباسورد مفعل رجائا ارسله للاستمرار", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("» وين جنت لخاطر ربك", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply("» الباسورد غلط.\n\عيد الاستخراج", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**هذا كود {ty} جلسه الخاص بك** \n\n`{string_session}` \n\n**تم انشائه من قبل:** @SXYO3\n ملاحظه لا تنطي الكود حتى لحبيبتك لان تدخل حسابك وتطلع كل خياساتك"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "» تم كود التيرمكس بنجاح {}\n\شوف رسايلك المحفوظه ! \n\n**تم انشاء الكود من قبل** @SXYO3 ".format("telethon" if telethon else "pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**» تم الغاء تكوين الجلسه !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**» تم اعادة تشغيل البوت بنجاح لاجلك 🪄 !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**» تم الغاء الجلسه !**", quote=True)
        return True
    else:
        return False
