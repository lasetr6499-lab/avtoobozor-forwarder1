import re
import logging
from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO)

API_ID = 31668984
API_HASH = 'd2a3a438612f36404fccc3f710712d6a'

# Kuzatiladigan kanallar ro'yxati (ID raqamlarini shu yerga vergul bilan qo'shasiz)
KUZATILADIGAN_KANALLAR = [
    -1001735935616,  # 1-kanal (hozirgi)
    -1002040364547,  # 2-kanal (yangi kanal ID si)
    -1003670560680   # 3-kanal (yangi kanal ID si)

]

MENING_KANALIM = -1003656600430

MENING_USERNAME = "@AVTOOBOZOR" 
MENING_LINK = "https://t.me/+KUwCjjg4ENg5Y2Iy"

client = TelegramClient('avto_bozor_session', API_ID, API_HASH)

# chats=KUZATILADIGAN_KANALLAR ro'yxatni to'liq qabul qiladi
@client.on(events.NewMessage(chats=KUZATILADIGAN_KANALLAR))
async def handler(event):
    try:
        matn = event.message.text or ""
        
        if matn:
            matn = re.sub(r'(https?://)?(t\.me|telegram\.me)/[a-zA-Z0-9_\+\-]+', MENING_LINK, matn)
            matn = re.sub(r'@[a-zA-Z0-9_]+', MENING_USERNAME, matn)

        await client.send_message(
            MENING_KANALIM,
            matn,
            file=event.message.media,
            formatting_entities=event.message.entities,
            buttons=None,
            link_preview=False
        )
        print(f"Post {event.chat_id} kanalidan olindi va muvaffaqiyatli o'tkazildi! ID: {event.message.id}")
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

print(f"{len(KUZATILADIGAN_KANALLAR)} ta kanalni kuzatish boshlandi...")
client.start()
client.run_until_disconnected()
