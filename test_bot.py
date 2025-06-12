import asyncio
from telegram import Bot

BOT_TOKEN = '8018888910:AAGQlpp-t0Z6LiVxTQ9Sa8C9YDhRW5rmkVo'  
CHAT_ID = 653066863  

bot = Bot(token=BOT_TOKEN)

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="Привіт! Бот працює з Render.")
    print("Повідомлення надіслано")

if __name__ == "__main__":
    asyncio.run(main())
