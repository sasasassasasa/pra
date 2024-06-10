from data_handler import load_chat_keywords, save_chat_keywords

chat_keywords = load_chat_keywords()


def register_message_handlers(bot):
    @bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
    def handle_media_message(message):
        chat_id = message.chat.id
        keyword = 'your_keyword_here'  # Определите, как вы хотите получить ключевое слово
        content = None

        if message.content_type == 'photo':
            content = message.photo[-1].file_id
        elif message.content_type == 'video':
            content = message.video.file_id
        elif message.content_type == 'document':
            content = message.document.file_id
        elif message.content_type == 'text':
            content = message.text

        if chat_id not in chat_keywords:
            chat_keywords[chat_id] = {}

        chat_keywords[chat_id][keyword] = {'type': message.content_type, 'content': content}
        save_chat_keywords(chat_keywords)

        bot.send_message(chat_id, f'Media with keyword "{keyword}" has been saved.')
