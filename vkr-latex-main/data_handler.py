import json

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Данные успешно загружены из {file_path}")
            return data
    except FileNotFoundError:
        print(f"{file_path} не найден. Начало с пустого словаря.")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON из {file_path}. Начало с пустого словаря.")
        return {}

def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {file_path}")

def load_banned_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            banned_words = json.load(file)
            print(f"Запрещенные слова успешно загружены из {file_path}")
            return banned_words
    except FileNotFoundError:
        print(f"{file_path} не найден. Начало с пустого списка запрещенных слов.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON из {file_path}. Начало с пустого списка запрещенных слов.")
        return []
