import json

def load_banned_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            banned_words = json.load(f)
        return banned_words
    except Exception as e:
        print(f"Error loading banned words from {file_path}: {e}")
        return []

def contains_banned_words(message, banned_words):
    return any(word in message for word in banned_words)

def contains_keywords(message, keywords):
    return any(keyword in message for keyword in keywords)
