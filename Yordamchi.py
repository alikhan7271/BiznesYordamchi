from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ChatAction
import asyncio

# Token va admin ID
TOKEN = "7921959076:AAEC5UCgFyCQMoP0WG1X_I-n1LHpxFzdWYE"
ADMIN_ID = 6541273111

# Bot va Dispatcher yaratamiz
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Asosiy menyu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📁 Hujjatlar")],
        [KeyboardButton(text="💼 Xizmatlar")],
        [KeyboardButton(text="📩 Murojaat yuborish")]
    ],
    resize_keyboard=True
)

# Hujjatlar ro'yxati
documents = {
    "MCHJ ochish uchun ariza": "https://example.com/MCHJ_ariza.docx",
    "Ishga qabul qilish shartnomasi": "https://example.com/Ishga_qabul_shartnoma.docx",
    "Grant loyihasi namunasi": "https://example.com/Grant_loyiha_namuna.docx",
    "Biznes reja namunasi": "https://example.com/Biznes_reja_namuna.docx",
}

# Xizmatlar ro'yxati
services = {
    "Logo chizish": "100 000 so‘m",
    "Sayt yaratish": "300 000 so‘m",
    "Telegram bot yaratish": "400 000 so‘m",
    "Yuridik maslahat": "50 000 so‘m",
    "Hujjat tayyorlash": "70 000 so‘m",
    "Grant bo‘yicha maslahat": "80 000 so‘m",
}

# /start buyrug'i uchun handler
@dp.message(Command(commands=["start"]))
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Men — Biznes Yordamchi botiman. Quyidagi bo‘limlardan birini tanlang:",
        reply_markup=main_menu,
    )

# "📁 Hujjatlar" tugmasi uchun handler
@dp.message(F.text == "📁 Hujjatlar")
async def documents_handler(message: types.Message):
    text = "Quyidagi hujjatlar mavjud:\n\n"
    for name in documents:
        text += f"• {name}\n"
    text += "\nKerakli hujjat nomini yozing, sizga havola yuboraman."
    await message.answer(text)

# Hujjat so‘ralganda havola yuborish
@dp.message(F.text.in_(documents.keys()))
async def send_document(message: types.Message):
    await bot.send_chat_action(message.chat.id, action=ChatAction.TYPING)
    doc_url = documents[message.text]
    await message.answer_document(types.FSInputFile.from_url(doc_url), caption=message.text)

# "💼 Xizmatlar" tugmasi uchun handler
@dp.message(F.text == "💼 Xizmatlar")
async def services_handler(message: types.Message):
    text = "Biz quyidagi xizmatlarni taklif qilamiz:\n\n"
    for name, price in services.items():
        text += f"• {name} — {price}\n"
    await message.answer(text)

# "📩 Murojaat yuborish" tugmasi uchun handler
@dp.message(F.text == "📩 Murojaat yuborish")
async def ask_contact(message: types.Message):
    await message.answer("Iltimos, murojaatingizni yozing. Biz tez orada javob beramiz.")

# Har qanday boshqa matnli xabarni qayta ishlash
@dp.message()
async def handle_message(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        log_text = (
            f"📥 Yangi murojaat:\n"
            f"👤 Ism: {message.from_user.full_name}\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"✉️ Xabar: {message.text}"
        )
        await bot.send_message(chat_id=ADMIN_ID, text=log_text)
        await message.answer("✅ Xabaringiz qabul qilindi, tez orada javob beramiz.")
    else:
        await message.answer("Salom, Admin! Siz bu yerda foydalanuvchilarning xabarlarini ko‘rishingiz mumkin.")

# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
