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

import config



ask_ques = "**📟اذا كنـت تـريد تنـصيـب
◍ مـيوزك فـأختـار كــود بـايـروجـرام
◍ التليثون فـأخـتار كــود تيرمكـس

◍ يتضمن ايضا البوت 
-: جلسه ميوزك قديمه وحديث. يوجد جلسات للبوتات بلاسفل **"
buttons_ques = [
    [
        InlineKeyboardButton("💻 : بـآيــروجــرآم", callback_data="pyrogram"),
        InlineKeyboardButton("💀 : تـليـثونہ", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("🤖 : بـآيروجـرآم للبــوت", callback_data="pyrogram_bot"),
        InlineKeyboardButton("🤖 : تـليـثونہ للʙᴏᴛ", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="🙄 آًسـتخرج آلجلـسة 🙄", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "ᴛᴇʟᴇᴛʜᴏɴ"
    else:
        ty = "ᴩʏʀᴏɢʀᴀᴍ"
    if is_bot:
        ty += " ʙᴏᴛ"
    await msg.reply(f"◍ جاري استخراج جلسه **{ty}** من البوت...√")
    user_id = msg.chat.id
    api_id_msg = await msg.chat.ask("🎮أولا قم بأرسال الـ API_ID\n\nاضغط /skip لـلـتـخـطـي", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**ᴀᴩɪ_ɪᴅ** ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ, sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await msg.chat.ask("» » 🎮حسنـا قم بأرسال الـ API_HASH", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "✔️الان ارسل رقمك مع رمز دولتك , مثال :+201099552517'"
    else:
        t = "ᴩʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ʙᴏᴛ_ᴛᴏᴋᴇɴ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\nᴇxᴀᴍᴩʟᴇ : `5432198765:abcdanonymousterabaaplol`'"
    phone_number_msg = await msg.chat.ask(t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("»⬇️انتـظر لـحظـه سـوف نـرسـل كـود لحسابـك بالتليجـرام")
    else:
        await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ ʟᴏɢɪɴ ᴠɪᴀ ʙᴏᴛ ᴛᴏᴋᴇɴ...")
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
        await msg.reply("» يقلب **ᴀᴩɪ_ɪᴅ** و **ᴀᴩɪ_ʜᴀsʜ** بتوع اك محذوف. \n\nاعمل استرت يقلب عشن تبدا من الاول.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("» يقلب **الرقم** مش معمول بيه اكونت اصلا علي التلي.\n\nاعمل استرت وابدا من الاول وابعت الرقم متخفش", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await msg.chat.ask("»»[شـوف آلصـورهہ‏‏ الكود مبعوت ازاي وابعت زيه عشان ميجيش ليك.ابطاء](https://telegra.ph/file/da1af082c6b754959ab47.jpg)» 🔍من فضلك افحص حسابك بالتليجرام وتفقد الكود من حساب اشعارات التليجرام. إذا كان\n  هناك تحقق بخطوتين( المرور ) ، أرسل كلمة المرور هنا بعد ارسال كود الدخول بالتنسيق أدناه.- اذا كانت كلمة المرور او الكود  هي\n 12345 يرجى ارسالها بالشكل التالي 1 2 3 4 5 مع وجود مسـافـات بين الارقام اذا احتجت مساعدة @Mahmod777777..", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("» لقد تخطـيـﮯت آلحد آلقصـيـﮯ 10 دقآيـﮯق\n\nآعمـل آسـترت عشـآن تسـتخرج مـن آلآول", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("» آلگود آل بعتهہ‏‏ غلطـ **رگز يـﮯقلب.**\n\nآعمـل آسـترت عشـآن تسـتخرج جلسـهہ‏‏ مـ آلآول", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("» آلگود مـنهہ‏‏يـﮯ **مدته انتهت.**\n\nآعمـل آسـترت عشـآن تسـتخرج جلسـهہ‏‏ مـ آلآول", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await msg.chat.ask("» آبعت **رمـز آلتحقق** بآسـورد آلآگ عشـآن .", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("» فآت 5 دقآيـﮯق.\n\nآنتهہ‏‏ت آلمـدهہ‏‏ آعمـل آسـترت وآبدآ مـ .", reply_markup=InlineKeyboardMarkup(gen_button))
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
                await two_step_msg.reply("» آلبآسـورد غلطـ يـﮯقلب\n\nآعمـل آسـترت وجرب تآنيـﮯ وآتآگد مـ ", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
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
    text = f"جلستك يبروو {ty} sᴛʀɪɴɢ sᴇssɪᴏɴ** \n\n`{string_session}` \n\n**ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ :** @Mahmod777777 \n🍒 **ɴᴏᴛᴇ :** حافظ عليها ممكن حد يخترقكك بيها\n اشترك بالحب @Ve_m1 🥺"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "» » ✅تم استخراج الجلسه بنجاح ️ {} .\n\n🔍من فضلك تفحص الرسايل المحفوظه بحسابك!  ! \n\n**𝙀𝙇𝙍𝘼𝙎𝘼𝙈 ‌𝅘𝅥𝅯** @Ve_m1 🥺".format("ᴛᴇʟᴇᴛʜᴏɴ" if telethon else "ᴩʏʀᴏɢʀᴀᴍ"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**» تم انهاء آلعمـليـﮯهہ‏‏**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**» تمـ آعآد‏‏هہ تشـغيـﮯل آلبوت !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**» تمـ آنهہ‏‏آء آلعمـليـﮯهہ‏‏!**", quote=True)
        return True
    else:
        return False
