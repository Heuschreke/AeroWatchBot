import requests
from telegram import Bot
import asyncio
import os
from dotenv import load_dotenv


date1, date2 = '2025-04-28', '2025-05-22'
arrival_iata1, arrival_iata2 = 'LED', 'AER'


# Переменная для хранения предыдущих данных
previous_data = dict.fromkeys([date1 + arrival_iata1, date2 + arrival_iata2], None)

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

# Функция для отправки сообщения в Telegram
async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def fetch_data(date, arrival_iata):
    '''
    В этой части происходит что-то недостижимое моего разума,\n
    отправляются какие-то запросы, на мой взгляд состоящие из иероглифов.\n
    Но, конечно, какие-то вещи я понимаю\n
    Например, "authorization" в словаре headers несет в себе инфу\n
    о токене запроса, он был выпущен 10.03.2025 и действует\n
    до 10.06.2025\n
    кукисы как бы повторяют этот токен\n
    хз, зачем они нужны, возможно будет работь и без них\n
    всю инфу я вытащила и сконпоновала благодаря киту\n
    я ему просто скинула код запроса, который нашла\n
    в коде страницы, а точнее F12/Network(сеть)/(Fetch/XHR)/nemo\n
    клик правой мышкой, копировать чет там cURL\n
    nemo - это как я поняла исполняемый запрос\n
    на странице их несколько, я выбрала тот,\n
    в котором не было привязки к ID запроса\n
    конкретно этот выводит информацию о минимальных ценах\n
    на промежуток дат: в коде запроса есть стартовая дата\n
    data[variables][params][segments][date] -> "date": "2025-04-28"\n
    и сколько еще дней вперед ему надо просчитать\n
    data[variables][params][daysCount] -> "daysCount": 5\n
    далее в запросе указываются коды аэропортов\n
    отправления "departure": {"iata": "NUX"} и\n
    прибытия "arrival": {"iata": "LED"}\n
    '''

    # URL API
    url = "https://yc.websky.aero/graphql/query/nemo"

    # Заголовки
    headers = {
        "accept": "*/*",
        "accept-language": "ru",
        "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wveWMud2Vic2t5LmFlcm9cL2dyYXBocWxcL3F1ZXJ5XC9uZW1vIiwiaWF0IjoxNzQxNzYwNzg0LCJleHAiOjE3NDk1MzY3ODQsIm5iZiI6MTc0MTc2MDc4NCwianRpIjoieGJTN2c3ZXZTS3dGTVZyMyIsInN1YiI6NzcyNTIyOCwicHJ2IjoiZGY4Zjk4NGEwNGUwYjc3NzcwYjBiMzZmNjQwOWFhZTVjMzJlODk1YSIsIm54MSI6IjdXT0JwMWtCSktSb2o4ODlkOVBSVDdnekFERWFzWGNSb1hDODRhZ0RYTVlWSmg4WXg0VWZwZ3RJYXdxdnRtZHl2RjBINm5mZ1VMRmJjd0pXZWNZSXUyVEpBWnk1d0ZZcjZaQTFScURvdGpEV05jdUVuQ2xvTFBOTnpDOWZnTU1hIiwibngzIjpbXSwibng0IjpmYWxzZX0.sOk4vVxZ9DByVuyen6uEtd1m-8SjkBGhOQR1GTrRxUI",
        "content-type": "application/json",
        "origin": "https://yamalaero.ru",
        "referer": "https://yamalaero.ru/booking/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
    }

    # Cookies
    cookies = {
        "hashed_value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wveWMud2Vic2t5LmFlcm9cL2dyYXBocWxcL3F1ZXJ5XC9uZW1vIiwiaWF0IjoxNzQxNzYwNzg0LCJleHAiOjE3NDk1MzY3ODQsIm5iZiI6MTc0MTc2MDc4NCwianRpIjoieGJTN2c3ZXZTS3dGTVZyMyIsInN1YiI6NzcyNTIyOCwicHJ2IjoiZGY4Zjk4NGEwNGUwYjc3NzcwYjBiMzZmNjQwOWFhZTVjMzJlODk1YSIsIm54MSI6IjdXT0JwMWtCSktSb2o4ODlkOVBSVDdnekFERWFzWGNSb1hDODRhZ0RYTVlWSmg4WXg0VWZwZ3RJYXdxdnRtZHl2RjBINm5mZ1VMRmJjd0pXZWNZSXUyVEpBWnk1d0ZZcjZaQTFScURvdGpEV05jdUVuQ2xvTFBOTnpDOWZnTU1hIiwibngzIjpbXSwibng0IjpmYWxzZX0.sOk4vVxZ9DByVuyen6uEtd1m-8SjkBGhOQR1GTrRxUI",
        "session_id": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wveWMud2Vic2t5LmFlcm9cL2dyYXBocWxcL3F1ZXJ5XC9uZW1vIiwiaWF0IjoxNzQxNzYwNzg0LCJleHAiOjE3NDk1MzY3ODQsIm5iZiI6MTc0MTc2MDc4NCwianRpIjoieGJTN2c3ZXZTS3dGTVZyMyIsInN1YiI6NzcyNTIyOCwicHJ2IjoiZGY4Zjk4NGEwNGUwYjc3NzcwYjBiMzZmNjQwOWFhZTVjMzJlODk1YSIsIm54MSI6IjdXT0JwMWtCSktSb2o4ODlkOVBSVDdnekFERWFzWGNSb1hDODRhZ0RYTVlWSmg4WXg0VWZwZ3RJYXdxdnRtZHl2RjBINm5mZ1VMRmJjd0pXZWNZSXUyVEpBWnk1d0ZZcjZaQTFScURvdGpEV05jdUVuQ2xvTFBOTnpDOWZnTU1hIiwibngzIjpbXSwibng0IjpmYWxzZX0.sOk4vVxZ9DByVuyen6uEtd1m-8SjkBGhOQR1GTrRxUI",
    }

    # Тело запроса (GraphQL)
    data = {
        "operationName": "FlightsMinPricesInPeriod",
        "variables": {
            "params": {
                "passengers": [
                    {"passengerType": "ADT", "extendedPassengerType": None, "count": 1},
                    {"passengerType": "CLD", "extendedPassengerType": None, "count": 0},
                    {"passengerType": "INF", "extendedPassengerType": None, "count": 0},
                    {"passengerType": "INS", "extendedPassengerType": None, "count": 0}
                ],
                "daysCount": 5,
                "segments": [
                    {
                        "date": date,
                        "departure": {"iata": "NUX"},
                        "arrival": {"iata": arrival_iata}
                    }
                ]
            }
        },
        "query": """
            query FlightsMinPricesInPeriod($params: FlightsMinPricesInPeriodParameters!) {
                FlightsMinPricesInPeriod(parameters: $params) {
                    datesWithLowestPrices {
                        date
                        info
                        price {
                            amount
                            currency
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }
        """
    }

    # Отправка POST-запроса
    response = requests.post(url, headers=headers, cookies=cookies, json=data)
    return response

async def fetch_and_send_data(date, arrival_iata):
    '''
    Здесь происходит еще одна магия,\n
    полученная информаци обрабатывается\n
    таким образом, как мне нужно\n
    по факту запрос я отправляю каждые 60 секунд\n
    и сравниваю с предыдущим ответом\n
    если ответы не совпадают, то ищу что именно изменилось,\n
    соответственно это я и отправляю пото в тг\n
    после запроса мне возвращается ответ, который я привожу\n
    к JSON виду и уже из него извлекаю нужную инфу\n
    просто обращаюсь к ключам словаря\n
    ['data']['FlightsMinPricesInPeriod']['datesWithLowestPrices']\n
    который возаращает список, содержащий даты\n
    и информацию о стоимости\n
    если в эту дату полет не выполняется или билетов нет,\n
    то в ключе ['price'] будет None\n
    в противном случае там будет цена на билет\n
    '''
    global previous_data

    # Уникальный ключ для каждого запроса
    key = date + arrival_iata

    # Получаем данные
    response = fetch_data(date, arrival_iata)

    # Проверка ответа
    if response.status_code == 200:
        try:
            # Парсим JSON-ответ
            response_data = response.json()['data']['FlightsMinPricesInPeriod']['datesWithLowestPrices']

            # Сравниваем полученные данные с предыдущими
            if response_data != previous_data[key]:
                message = f"Обнаружены изменения в ценах на билеты по направлению {arrival_iata}:\n"
                if previous_data[key] is not None:
                    for i, j in zip(previous_data[key], response_data):
                        if i != j:
                            if j['price'] is not None:
                                message += f"Дата: {j['date']}, Цена: {j['price']['amount']}\n"
                            else:
                                message += f"Дата: {j['date']}, Билетов нет"

                else:
                    # Если это первый запрос, просто сохраняем данные
                    message = f"Начало работы программы:)\nПо направлению в {arrival_iata} инфа такая:\n"

                    for i in response_data:
                        if i['price'] is not None:
                            message += f"Дата: {i['date']}, Цена: {i['price']['amount']}\n"
                        else:
                            message += f"Дата: {i['date']}, Билетов нет\n"
                    message += 'Я сообщу, если что-то изменится'

                # Обновляем предыдущие данные
                previous_data[key] = response_data

                # Отправляем собранную информацию в Telegram
                await send_telegram_message(message)

            else:
                print(f"Изменений нет для ({date}, {arrival_iata}).")

        # Обрабатываем ошибки
        except KeyError as e:
            print(f"Ошибка: ключ {e} отсутствует в ответе API.")
        except Exception as e:
            print(f"Ошибка при обработке ответа: {e}")
    else:
        print(f"Ошибка: {response.status_code}")

# Основной цикл
async def main():
    try:
        while True:
            # Запуск двух запросов параллельно с разными параметрами
            await asyncio.gather(
                fetch_and_send_data(date1, arrival_iata1),  # Первый запрос
                fetch_and_send_data(date2, arrival_iata2)   # Второй запрос
            )

            await asyncio.sleep(60)  # Задержка в 1 минута (60 секунд)
    except KeyboardInterrupt:
        # Отправляем сообщение при завершении программы
        await send_telegram_message("На данный момент программа завершена")
        print("Программа завершена пользователем.")

# Запуск асинхронного кода
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        # Обработка KeyboardInterrupt на уровне event loop
        loop.run_until_complete(send_telegram_message("На данный момент программа завершена"))
        print("Программа завершена пользователем.")
    finally:
        loop.close()