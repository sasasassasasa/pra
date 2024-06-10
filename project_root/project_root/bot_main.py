import os
from telebot import TeleBot
from command_handlers import register_command_handlers
from weather_handler import register_weather_handlers, send_daily_weather
from data_handler import load_data
import schedule

# Инициализация бота
bot_token = '6844853072:AAE9E21vq017QAWP_9ZSNBF-0460bLBFChM'
bot = TeleBot(bot_token)
data_file_path = 'chat_keywords.json'

# Загрузка сохраненных данных
chat_keywords = load_data(data_file_path)

# Регистрация командных обработчиков
register_command_handlers(bot, chat_keywords, data_file_path)
register_weather_handlers(bot)

# Настройка расписания для ежедневного отправления погоды
schedule.every().day.at("09:00").do(send_daily_weather, bot=bot)

# Запуск бота
if __name__ == '__main__':
    while True:
        schedule.run_pending()
        bot.polling(none_stop=True)
