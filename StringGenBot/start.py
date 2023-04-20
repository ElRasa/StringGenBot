from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""📟¦اهلا بـك عزيـزي 📬 {msg.from_user.mention}

مرحبا في {me2}
⚡¦يـمكنك استـخـراج الـتـالـي
♻️¦تيرمـكـس تليثون للحسـابـات🏂
♻️¦تيرمـكـس تليثون للبوتــات🤖
🎧¦بايـروجـرام مـيوزك للحسابات🙋🏼‍♂️
🗽¦بايـروجـرام مـيوزك احدث اصدار🎊
🎧¦بايـروجـرام مـيوزك للبوتات🤖
-  تم انشـاء هـذا البـوت بواسطـة:  [ᯓ『 𝙀𝙇𝙍𝘼𝙎𝘼𝙈 ‌𝅘𝅥𝅯 』🇵🇸𓆃](tg://user?id={OWNER_ID}) !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="🌐:آضـغـــط لَبــدآ آًستـــخـرآج كود", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("ً⚙ً.. آلـســــورس", url="https://t.me/Ve_m1"),
                    InlineKeyboardButton("ᯓ『 𝙀𝙇𝙍𝘼𝙎𝘼𝙈 ‌𝅘𝅥𝅯』🏴󠁧󠁢󠁥󠁮󠁧󠁿𓆃", user_id=OWNER_ID)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
