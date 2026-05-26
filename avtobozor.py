import re
import logging
import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

# Konsolda jarayonlarni kuzatish uchun loglar
logging.basicConfig(level=logging.INFO)

# ==========================================
# 1. SOZLAMALAR (MAXFIY KALITLARSIZ)
# ==========================================
# Barcha maxfiy ma'lumotlar faqat Render ENV bo'limidan o'qiladi!
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("TELEGRAM_SESSION")

# Agar Render'da ENV kiritilmagan bo'lsa, xatolik chiqib kod to'xtaydi
if API_ID:
    API_ID = int(API_ID)

# Kuzatiladigan kanallar ro'yxati (Kanal ID raqamlari)
KUZATILADIGAN_KANALLAR = [
    -1001735935616,
    -1002040364547,
    # Agar yana kanal qo'shmoqchi bo'lsangiz, pastiga vergul bilan yozasiz
]

MENING_KANALIM = -1003656600430
MENING_USERNAME = "@AVTOOBOZOR" 
MENING_LINK = "https://t.me/+KUwCjjg4ENg5Y2Iy"

# ==========================================
# 2. USERBOT KLIENTINI INICIALIZATSIYA QILISH
# ==========================================
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats=KUZATILADIGAN_KANALLAR))
async def handler(event):
    try:
        matn = event.message.text or ""
        if matn:
            # 1. Matndagi begona telegram havolalarini sizning kanalingiz linkiga almashtirish
            matn = re.sub(r'(https?://)?(t\.me|telegram\.me)/[a-zA-Z0-9_\+\-]+', MENING_LINK, matn)
            # 2. Eskicha @username'larni o'z kanalingiz nomiga almashtirish
            matn = re.sub(r'@[a-zA-Z0-9_]+', MENING_USERNAME, matn)

        # Xabarni formati, mediasi va stillari bilan sizning kanalingizga yuborish
        await client.send_message(
            MENING_KANALIM,
            matn,
            file=event.message.media,
            formatting_entities=event.message.entities, # Shrift stillarini saqlash
            buttons=None,                                # Tugmalarni o'chirib tashlash
            link_preview=False                           # Havola prevyusini ko'rsatmaslik
        )
        print("Post muvaffaqiyatli tahrirlanib o'tkazildi!")
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

# ==========================================
# 3. RENDER VEB-SERVER (UYG'OQ TURISH LOGIKASI)
# ==========================================
async def handle(request):
    return web.Response(text="AvtoObozor skripti muvaffaqiyatli va xavfsiz ishlamoqda!")

async def start_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Veb-server {port}-portda muvaffaqiyatli ishga tushdi.")

# ==========================================
# 4. ASOSIY ISHGA TUSHIRISH (MAIN)
# ==========================================
async def main():
    print("Telegram Userbot ishga tushmoqda...")
    
    # Xavfsizlik tekshiruvlari
    if not API_ID or not API_HASH:
        print("XATOLIK: API_ID yoki API_HASH Render ENV bo'limiga kiritilmagan!")
        return
        
    if not STRING_SESSION:
        print("XATOLIK: TELEGRAM_SESSION kaliti Render ENV bo'limiga kiritilmagan!")
        return

    await client.connect()
    if not await client.is_user_authorized():
        print("XATOLIK: Render ENV ichidagi TELEGRAM_SESSION kaliti eskirgan yoki xato!")
        return
        
    print("Userbot muvaffaqiyatli va XAVFSIZ ulandi! Kanallar kuzatilmoqda...")
    
    # Serverni va kanallar monitoringini parallel yuritish
    await asyncio.gather(start_server(), client.run_until_disconnected())

if __name__ == '__main__':
    asyncio.run(main())
