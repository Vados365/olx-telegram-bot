import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio

# Витягуємо токен і chat_id з середовища, або використовуємо значення по замовчуванню
TOKEN = os.getenv("TOKEN", "8018888910:AAGQlpp-t0Z6LiVxTQ9Sa8YDhRW5rmkVo")
CHAT_ID = int(os.getenv("CHAT_ID", 653066863))

bot = Bot(token=TOKEN)
URL = "https://www.olx.ua/uk/list/q-iphone-11/?search%5Bfilter_float_price%3Afrom%5D=3500&search%5Bfilter_float_price%3Ato%5D=6000"
HEADERS = {"User-Agent": "Mozilla/5.0"}

seen_ads = set()

def fetch_ads():
    ads = []
    try:
        response = requests.get(URL, headers=HEADERS)
        print("Status code:", response.status_code)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.select("div[data-cy='l-card']")
        print(f"Знайдено оголошень: {len(cards)}")
        for card in cards:
            title_elem = card.select_one("h6")
            price_elem = card.select_one("p[data-testid='ad-price']")
            link_elem = card.select_one("a")

            if title_elem and price_elem and link_elem:
                title = title_elem.get_text(strip=True)
                price = price_elem.get_text(strip=True)
                link = "https://www.olx.ua" + link_elem['href']
                ad_id = link.split("-")[-1].replace(".html", "")

                if ad_id not in seen_ads:
                    seen_ads.add(ad_id)
                    ads.append((title, price, link))
    except Exception as e:
        print("Помилка при парсингу OLX:", e)
    return ads

async def main():
    print("Бот запущено.")

    try:
        await bot.send_message(chat_id=CHAT_ID, text="OLX бот запущено ✅")
    except Exception as e:
        print("Не вдалося надіслати стартове повідомлення:", e)

    while True:
        new_ads = fetch_ads()
        if new_ads:
            for title, price, link in new_ads:
                message = f"🔔 Нове оголошення:\n\n📱 {title}\n💰 Ціна: {price}\n🔗 {link}"
                try:
                    await bot.send_message(chat_id=CHAT_ID, text=message)
                    print(f"Надіслано: {title}")
                except Exception as e:
                    print("Помилка надсилання:", e)
        else:
            print("Нових оголошень немає.")
        await asyncio.sleep(300)  # 5 хвилин

if __name__ == "__main__":
    asyncio.run(main())
