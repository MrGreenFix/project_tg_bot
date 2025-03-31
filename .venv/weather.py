import requests
import datetime

# from pprint import pprint
from config import TOKEN_WEATHER
from time import strftime


def get_weather(city, TOKEN_WEATHER):

    code_to_smile = {"Clear": "Ясно\U00002600",
                     "Clouds": "Облачно\U00002601",
                     "Rain": "Дождь\U00002614",
                     "Drizzle": "Морось\U00002614",
                     "Thunderstorm": "Гроза\U000026A1",
                     "Snow": "Снег\U0001F328",
                     "Mist": "Туман\U0001F32B"
                     }


    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={TOKEN_WEATHER}&units=metric")
        data = r.json()



        city = data["name"]
        temp_city = data["main"]["temp"]

        weather_state = data["weather"][0]["main"]
        if weather_state in code_to_smile:
            wd = code_to_smile[weather_state]
        else:
            wd = "Это не описать словами, сам посмотри в окно!"

        humidity = data["main"]["humidity"]
        pressure = round(data["main"]["pressure"] * 0.75006)
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
        length_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])


        result = (f'***{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
            f'Погода в городе: {city}\nТемпература: {temp_city} C {wd}\n'
            f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind}\n'
            f'Восход солнца: {sunrise}\nЗакат: {sunset}\nПродолжительность дня: {length_day}')
        return result

    except Exception as ex:
        return f"⚠ Ошибка: {ex}\nПроверь название города."



