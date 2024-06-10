import requests
import json
from datetime import datetime
from telebot import TeleBot

WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
CURRENT_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = 'b95abfcd1e186f22560a271a013b1d2b'
WEATHER_FILE = 'weather_config.json'


def load_weather_config():
    try:
        with open(WEATHER_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_weather_config(data):
    with open(WEATHER_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'cnt': 8  # Получаем прогноз на 24 часа (8 временных точек по 3 часа)
    }
    response = requests.get(WEATHER_API_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_data = []
        for entry in data['list']:
            dt = datetime.fromtimestamp(entry['dt'])
            temp = entry['main']['temp']
            description = entry['weather'][0]['description']
            rain = entry.get('rain', {}).get('3h', 0)
            weather_data.append((dt, temp, description, rain))
        return weather_data
    else:
        return None


def get_current_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(CURRENT_WEATHER_API_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        dt = datetime.fromtimestamp(data['dt'])
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        rain = data.get('rain', {}).get('1h', 0)
        return (dt, temp, description, rain)
    else:
        return None


def format_weather_message(weather_data):
    message = "Погода на сегодня:\n"
    for dt, temp, description, rain in weather_data:
        time_of_day = dt.strftime("%H:%M")
        message += f"{time_of_day}: Температура {temp}°C, {description}, вероятность осадков {rain}%\n"
    return message


def format_current_weather_message(weather_data):
    dt, temp, description, rain = weather_data
    message = f"Текущая погода на {dt.strftime('%Y-%m-%d %H:%M')}:\nТемпература: {temp}°C\nОписание: {description}\nВероятность осадков: {rain}%"
    return message


def send_daily_weather(bot: TeleBot):
    config = load_weather_config()
    for chat_id, city in config.items():
        weather_data = get_weather(city)
        if weather_data:
            message = format_weather_message(weather_data)
            bot.send_message(chat_id, message)


def set_weather_city(bot: TeleBot, message):
    chat_id = str(message.chat.id)
    city = message.text.strip()

    config = load_weather_config()
    config[chat_id] = city
    save_weather_config(config)

    bot.send_message(chat_id, f"Город '{city}' выбран для отправки погоды.")


def get_and_send_current_weather(bot: TeleBot, message):
    chat_id = str(message.chat.id)
    config = load_weather_config()
    city = config.get(chat_id)

    if city:
        weather_data = get_current_weather(city)
        if weather_data:
            message = format_current_weather_message(weather_data)
            bot.send_message(chat_id, message)
        else:
            bot.send_message(chat_id, f"Не удалось получить текущую погоду для города '{city}'.")
    else:
        bot.send_message(chat_id, "Сначала установите город с помощью команды /set_city")


def register_weather_handlers(bot: TeleBot):
    @bot.message_handler(commands=['set_city'])
    def handle_set_city(message):
        bot.reply_to(message, "Введите город, по которому я буду отправлять погоду.")
        bot.register_next_step_handler(message, lambda msg: set_weather_city(bot, msg))

    @bot.message_handler(commands=['current_weather'])
    def handle_current_weather(message):
        get_and_send_current_weather(bot, message)

    @bot.message_handler(commands=['change_city'])
    def handle_change_city(message):
        bot.reply_to(message, "Введите новый город для получения погоды.")
        bot.register_next_step_handler(message, lambda msg: set_weather_city(bot, msg))
