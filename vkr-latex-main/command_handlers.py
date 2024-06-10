import os
import pathlib
from telebot import TeleBot
from data_handler import save_data, load_banned_words
from filter import contains_banned_words, contains_keywords
from pathlib import Path
from weather_handler import register_weather_handlers

user_states = {}


def register_command_handlers(bot: TeleBot, chat_keywords, file_path):
    # Регистрация всех командных обработчиков
    register_weather_handlers(bot)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, (
            "Я бот, который может сохранять и отправлять сообщения, связанные с ключевыми словами. "
            "Команды:\n"
            "/save <ключевое слово> - сохранить сообщение или изображение\n"
            "/edit <ключевое слово> - редактировать сообщение\n"
            "/del <ключевое слово> - удалить сообщение\n"
            "/list - показать все ключевые слова\n"
            "/save_w <ключевое слово> - сохранить сообщение или изображение с возможностью уведомления\n"
            "/edit_w <ключевое слово> - редактировать сообщение с возможностью уведомления\n"
            "/del_w <ключевое слово> - удалить сообщение с возможностью уведомления\n"
            "/list_w - показать все ключевые слова с возможностью уведомления\n"
            "/weather <город> - получить текущую погоду для указанного города\n"
            "/set_city - Установить город для прогноза погоды\n"
            "/current_weather - Получить текущую погоду\n"
            "/change_city - Изменить город для получения погоды\n"
            "Когда кто-то напишет ключевое слово, я отправлю сохраненное сообщение. "
            "Я также удаляю сообщения, содержащие запрещенные слова."
        ))

    @bot.message_handler(commands=['save'])
    def save_keyword(message):
        try:
            chat_id = str(message.chat.id)
            user_id = message.from_user.id
            keyword = message.text.split(' ', 1)[1].strip()

            if chat_id not in chat_keywords:
                chat_keywords[chat_id] = {}

            if keyword in chat_keywords[chat_id]:
                bot.reply_to(message,
                             f"Ключевое слово '{keyword}' уже существует. Используйте команду /edit для редактирования.")
            else:
                bot.reply_to(message,
                             f"Ключевое слово '{keyword}' сохранено, ожидаю информацию или изображение для сохранения.")
                user_states[(chat_id, user_id)] = ('save', keyword)

        except IndexError:
            bot.reply_to(message, "Пожалуйста, укажите ключевое слово после команды /save.")

    @bot.message_handler(commands=['save_w'])
    def save_w_keyword(message):
        try:
            chat_id = str(message.chat.id)
            user_id = message.from_user.id
            keyword = message.text.split(' ', 1)[1].strip()

            if chat_id not in chat_keywords:
                chat_keywords[chat_id] = {}
            if 'w' not in chat_keywords[chat_id]:
                chat_keywords[chat_id]['w'] = {}

            if keyword in chat_keywords[chat_id]['w']:
                bot.reply_to(message,
                             f"Ключевое слово '{keyword}' уже существует. Используйте команду /edit_w для редактирования.")
            else:
                bot.reply_to(message,
                             f"Ключевое слово '{keyword}' сохранено, ожидаю информацию или изображение для сохранения.")
                user_states[(chat_id, user_id)] = ('save_w', keyword)

        except IndexError:
            bot.reply_to(message, "Пожалуйста, укажите ключевое слово после команды /save_w.")

    @bot.message_handler(commands=['edit'])
    def edit_keyword(message):
        try:
            chat_id = str(message.chat.id)
            user_id = message.from_user.id
            keyword = message.text.split(' ', 1)[1].strip()

            if chat_id not in chat_keywords or keyword not in chat_keywords[chat_id]:
                bot.reply_to(message, f"Ключевое слово '{keyword}' не найдено.")
            else:
                bot.reply_to(message,
                             f"Редактирование ключевого слова '{keyword}'. Ожидаю новое сообщение или изображение для сохранения.")
                user_states[(chat_id, user_id)] = ('edit', keyword)

        except IndexError:
            bot.reply_to(message, "Пожалуйста, укажите ключевое слово после команды /edit.")

    @bot.message_handler(commands=['edit_w'])
    def edit_w_keyword(message):
        try:
            chat_id = str(message.chat.id)
            user_id = message.from_user.id
            keyword = message.text.split(' ', 1)[1].strip()

            if chat_id not in chat_keywords or 'w' not in chat_keywords[chat_id] or keyword not in \
                    chat_keywords[chat_id]['w']:
                bot.reply_to(message, f"Ключевое слово '{keyword}' не найдено.")
            else:
                bot.reply_to(message,
                             f"Редактирование ключевого слова '{keyword}' с возможностью уведомления. Ожидаю новое сообщение или изображение для сохранения.")
                user_states[(chat_id, user_id)] = ('edit_w', keyword)

        except IndexError:
            bot.reply_to(message, "Пожалуйста, укажите ключевое слово после команды /edit_w.")

    @bot.message_handler(commands=['del'])
    def del_keyword(message):
        try:
            chat_id = str(message.chat.id)
            keyword = message.text.split(' ', 1)[1].strip()

            if chat_id in chat_keywords and keyword in chat_keywords[chat_id]:
                del chat_keywords[chat_id][keyword]
                bot.reply_to(message, f"Ключевое слово '{keyword}' удалено.")
                save_data(chat_keywords, file_path)
            else:
                bot.reply_to(message, f"Ключевое слово '{keyword}' не найдено.")

        except IndexError:
            bot.reply_to(message, "Пожалуйста, укажите ключевое слово после команды /del.")

    @bot.message_handler(commands=['del_w'])
    def del_w_keyword(message):
        try:
            chat_id = str(message.chat.id)
            keyword = message.text.split(' ', 1)[1].strip()

            if chat_id in chat_keywords and 'w' in chat_keywords[chat_id] and keyword in chat_keywords[chat_id]['w']:
                del chat_keywords[chat_id]['w'][keyword]
                bot.reply_to(message, f"Ключевое слово '{keyword}' с возможностью уведомления удалено.")
                save_data(chat_keywords, file_path)
            else:
                bot.reply_to(message, f"Ключевое слово '{keyword}' не найдено.")

        except IndexError:
            bot.reply_to(message, "Пожалуйста, укажите ключевое слово после команды /del_w.")

    @bot.message_handler(commands=['list'])
    def list_keywords(message):
        chat_id = str(message.chat.id)
        if chat_id in chat_keywords and chat_keywords[chat_id]:
            keywords = '\n'.join(chat_keywords[chat_id].keys())
            bot.reply_to(message, f"Ключевые слова:\n{keywords}")
        else:
            bot.reply_to(message, "Нет сохраненных ключевых слов.")

    @bot.message_handler(commands=['list_w'])
    def list_w_keywords(message):
        chat_id = str(message.chat.id)
        if chat_id in chat_keywords and 'w' in chat_keywords[chat_id] and chat_keywords[chat_id]['w']:
            keywords = '\n'.join(chat_keywords[chat_id]['w'].keys())
            bot.reply_to(message, f"Ключевые слова с возможностью уведомления:\n{keywords}")
        else:
            bot.reply_to(message, "Нет сохраненных ключевых слов с возможностью уведомления.")

    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        try:
            chat_id = str(message.chat.id)
            user_id = message.from_user.id
            state = user_states.get((chat_id, user_id))

            # Если пользователь в состоянии сохранения или редактирования, сохранить изображение
            if state:
                action, keyword = state
                Path(f'files/{chat_id}/').mkdir(parents=True, exist_ok=True)
                file_info = bot.get_file(message.photo[-1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = f'files/{chat_id}/' + file_info.file_path.replace('photos/', '')
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                if action == 'save':
                    chat_keywords[chat_id][keyword] = {'type': 'photo', 'path': src}
                    bot.reply_to(message, f"Фотография для ключевого слова '{keyword}' сохранена.")
                elif action == 'save_w':
                    chat_keywords[chat_id]['w'][keyword] = {'type': 'photo', 'path': src}
                    bot.reply_to(message,
                                 f"Фотография для ключевого слова '{keyword}' с возможностью уведомления сохранена.")
                elif action == 'edit':
                    chat_keywords[chat_id][keyword] = {'type': 'photo', 'path': src}
                    bot.reply_to(message, f"Фотография для ключевого слова '{keyword}' обновлена.")
                elif action == 'edit_w':
                    chat_keywords[chat_id]['w'][keyword] = {'type': 'photo', 'path': src}
                    bot.reply_to(message,
                                 f"Фотография для ключевого слова '{keyword}' с возможностью уведомления обновлена.")

                save_data(chat_keywords, file_path)
                del user_states[(chat_id, user_id)]
            else:
                bot.reply_to(message, "Фото получено, но не указано ключевое слово.")

        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка при обработке фото: {e}")

    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        chat_id = str(message.chat.id)
        user_id = message.from_user.id
        state = user_states.get((chat_id, user_id))

        banned_words = load_banned_words("banned_words.json")

        if contains_banned_words(message.text, banned_words):
            bot.delete_message(chat_id, message.message_id)
            bot.reply_to(message, "Ваше сообщение было удалено, так как оно содержит запрещенные слова.")
            return

        if state:
            action, keyword = state
            if action in ['save', 'save_w']:
                bot.reply_to(message, f"Сообщение для ключевого слова '{keyword}' сохранено.")
                if action == 'save':
                    chat_keywords[chat_id][keyword] = {'type': 'text', 'content': message.text}
                elif action == 'save_w':
                    chat_keywords[chat_id]['w'][keyword] = {'type': 'text', 'content': message.text}
            elif action in ['edit', 'edit_w']:
                bot.reply_to(message, f"Сообщение для ключевого слова '{keyword}' обновлено.")
                if action == 'edit':
                    chat_keywords[chat_id][keyword] = {'type': 'text', 'content': message.text}
                elif action == 'edit_w':
                    chat_keywords[chat_id]['w'][keyword] = {'type': 'text', 'content': message.text}

            save_data(chat_keywords, file_path)
            del user_states[(chat_id, user_id)]

        elif chat_id in chat_keywords:
            for keyword, content in chat_keywords[chat_id].items():
                if keyword in message.text:
                    if content['type'] == 'text':
                        bot.reply_to(message, content['content'])
                    elif content['type'] == 'photo':
                        with open(content['path'], 'rb') as photo:
                            bot.send_photo(chat_id, photo)

            if 'w' in chat_keywords[chat_id]:
                for keyword, content in chat_keywords[chat_id]['w'].items():
                    if contains_keywords(message.text, [keyword]):
                        if content['type'] == 'text':
                            bot.reply_to(message, content['content'])
                        elif content['type'] == 'photo':
                            with open(content['path'], 'rb') as photo:
                                bot.send_photo(chat_id, photo)

    return bot
