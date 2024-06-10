# file_buffer.py
import os
import pathlib
from pathlib import Path

FILE_BUFFER_DIR = "files"


def initialize_buffer():
    if not os.path.exists(FILE_BUFFER_DIR):
        os.makedirs(FILE_BUFFER_DIR)


def save_file(chat_id, file_info, bot, file_type):
    Path(f'{FILE_BUFFER_DIR}/{chat_id}/').mkdir(parents=True, exist_ok=True)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)
    src = f'{FILE_BUFFER_DIR}/{chat_id}/' + file_path.replace('photos/', '').replace('videos/', '').replace(
        'animations/', '')

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    return src


def get_file_path(chat_id, file_name):
    file_path = f'{FILE_BUFFER_DIR}/{chat_id}/{file_name}'
    if os.path.exists(file_path):
        return file_path
    return None


def remove_file(chat_id, file_name):
    file_path = get_file_path(chat_id, file_name)
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
