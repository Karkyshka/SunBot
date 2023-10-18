from telegram import Bot
import requests
import schedule
import time
from dotenv import load_dotenv
import datetime
import os
load_dotenv()


bot = Bot(os.getenv('TOKEN'))
chat_id = os.getenv('CHAT_ID')
# Данный о восходе солнца на сегодняшний день
URL_TDA = os.getenv('URL_TDA')
# Данный о восходе солнца на вчерашний день
URL_YDA = os.getenv('URL_YDA')


def get_sun():
    # Длина светового дня сегодня
    day_length_today = datetime.datetime.strptime(
        requests.get(URL_TDA).json()['results']['day_length'], '%H:%M:%S'
    )
    # Длина светового вчера
    day_length_yda = datetime.datetime.strptime(
        requests.get(URL_YDA).json()['results']['day_length'],  '%H:%M:%S'
    )
    # Разница в световом дне относительно вчера
    day_length = (((day_length_today-day_length_yda).total_seconds())/60)
    if day_length < 0:
        message = (
            f'Сегодня день стал короче на {abs(round(day_length, 2))} минуты'
        )
    if day_length > 0:
        message = (
            f'+{abs(round(day_length, 2))} к световому дню! '
        )
    if day_length == 0:
        message = ('А у нас дни солнцестояния!')
    return bot.send_message(chat_id, message)


# Задаем время отправки сообщения
schedule.every().day.at('08:41').do(get_sun)

# Бесконечный цикл для проверки расписания
while True:
    schedule.run_pending()
    time.sleep(1)
