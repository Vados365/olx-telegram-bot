import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time

TOKEN = "8018888910:AAGQlpp-t0Z6LiVxTQ9Sa8C9YDhRW5rmkVo"
CHAT_ID = 653066863

bot = Bot(token=TOKEN)
URL = "https://www.olx.ua/uk/list/q-iphone-11/?search%5Bfilter_float_price%3Afrom%5D=3500&search%5Bfilter_float_price%3Ato%5D=6000"
HEADERS = {"User-Agent": "Mozilla/5.0"}

seen_ads = set()  # Для збереження унікальних оголошень

def fetch_ads():
    ads = []
    try:
        response = requests.get(URL, headers=HEADERS)
        print("Status code:", response.status_code)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.select("div[data-cy='l-card']")
        print(f"Знайдено оголошень на сторінці: {len(cards)}")
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
    print(f"Нові оголошення для відправки: {len(ads)}")
    return ads

def main():
    print("Запуск OLX Telegram бота...")
    # Пробне повідомлення на старті
    try:
        bot.send_message(chat_id=CHAT_ID, text="Бот запущений і готовий надсилати повідомлення.")
    except Exception as e:
        print("Помилка при відправці стартового повідомлення:", e)
        return

    while True:
        new_ads = fetch_ads()
        if new_ads:
            for title, price, link in new_ads:
                message = f"Нове оголошення:\n{title}\nЦіна: {price}\n{link}"
                try:
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    print(f"Відправлено: {title}")
                except Exception as e:
                    print("Помилка при відправці повідомлення:", e)
        else:
            print("Нових оголошень немає.")
        time.sleep(300)  # чекати 5 хвилин

if __name__ == "__main__":
    main()
