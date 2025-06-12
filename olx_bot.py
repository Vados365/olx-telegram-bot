import requests
from bs4 import BeautifulSoup
import asyncio
from telegram import Bot

BOT_TOKEN = '8018888910:AAGQlpp-t0Z6LiVxTQ9Sa8C9YDhRW5rmkVo'
CHAT_ID = 6458514686

URL = 'https://www.olx.ua/uk/list/q-iphone-11/?search%5Bfilter_float_price%3Afrom%5D=3500&search%5Bfilter_float_price%3Ato%5D=6000'

sended_ads = set()

bot = Bot(token=BOT_TOKEN)

def get_ads():
    response = requests.get(URL)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    ads = soup.find_all('div', class_='css-1sw7q4x')

    new_ads = []
    for ad in ads:
        title_tag = ad.find('h6')
        link_tag = ad.find('a', href=True)
        price_tag = ad.find('p', class_='css-10b0gli')

        if not title_tag or not link_tag or not price_tag:
            continue

        title = title_tag.text.strip()
        link = 'https://www.olx.ua' + link_tag['href']
        price = price_tag.text.strip()

        ad_id = link.split('-ID')[1].split('.')[0] if '-ID' in link else link

        if ad_id not in sended_ads:
            new_ads.append((title, price, link))
            sended_ads.add(ad_id)

    return new_ads

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="Бот запущений і готовий надсилати повідомлення.")
    print("Запуск OLX Telegram бота...")

    while True:
        new_ads = get_ads()
        print("Нові оголошення для відправки:", len(new_ads))

        if new_ads:
            for title, price, link in new_ads:
                message = f"📱 {title}\n💰 {price}\n🔗 {link}"
                await bot.send_message(chat_id=CHAT_ID, text=message)
                await asyncio.sleep(1)
        else:
            print("Нових оголошень немає.")

        await asyncio.sleep(300)  # чекати 5 хвилин без блокування

if __name__ == '__main__':
    asyncio.run(main())
