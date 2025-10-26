import sqlite3
import time

# Настройка таймаута для подключений к БД
DB_TIMEOUT = 10.0


def db_create_words():
    with sqlite3.connect("db/material.db", timeout=DB_TIMEOUT) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS words_en(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            transkription TEXT NOT NULL,    
            perevod TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            age INT NOT NULL,
            role TEXT NOT NULL 
        )
        """)


def db_insert_word_en(word, transkription, pervod):
    with sqlite3.connect("db/material.db", timeout=DB_TIMEOUT) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO words_en (word,transkription,perevod) VALUES (?, ?, ?)",
            (word, transkription, pervod),
        )
        conn.commit()


def db_insert_users(persona):
    max_retries = 3
    for attempt in range(max_retries):
        conn = None
        try:
            conn = sqlite3.connect("db/material.db", timeout=DB_TIMEOUT)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (login,password,age,role) VALUES (?, ?, ?, ?)",
                (persona.login, persona.password, persona.age, persona.role),
            )
            conn.commit()
            return
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < max_retries - 1:
                time.sleep(0.2)
                continue
            raise
        finally:
            if conn:
                conn.close()


def db_get_user(login, password):
    """Получить пользователя по логину и паролю"""
    with sqlite3.connect("db/material.db", timeout=DB_TIMEOUT) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT login, password, age, role FROM users WHERE login = ? AND password = ?",
            (login, password),
        )
        result = cursor.fetchone()

        if result:
            return {
                "login": result[0],
                "password": result[1],
                "age": result[2],
                "role": result[3],
            }
        return None


def db_check_user_exists(login):
    """Проверить существует ли пользователь с данным логином"""
    with sqlite3.connect("db/material.db", timeout=DB_TIMEOUT) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT login FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()
        return result is not None


def db_insert_user_simple(login, password, age, role):
    """Простая регистрация пользователя"""
    max_retries = 3
    for attempt in range(max_retries):
        conn = None
        try:
            conn = sqlite3.connect("db/material.db", timeout=DB_TIMEOUT)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (login,password,age,role) VALUES (?, ?, ?, ?)",
                (login, password, age, role),
            )
            conn.commit()
            return  # Успешно выполнено
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < max_retries - 1:
                time.sleep(0.2)  # Увеличиваем задержку
                continue
            raise  # Повторяем ошибку если попытки исчерпаны
        finally:
            if conn:
                conn.close()


def db_insert_words_batch(words_list):
    """Массовая вставка слов в базу данных"""
    max_retries = 3
    for attempt in range(max_retries):
        conn = None
        try:
            conn = sqlite3.connect("db/material.db", timeout=DB_TIMEOUT)
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT INTO words_en (word, transkription, perevod) VALUES (?, ?, ?)",
                words_list,
            )
            conn.commit()
            return
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < max_retries - 1:
                time.sleep(0.2)
                continue
            raise
        finally:
            if conn:
                conn.close()


def db_check_word_exists(word):
    """Проверить существует ли слово в базе"""
    with sqlite3.connect("db/material.db", timeout=DB_TIMEOUT) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT word FROM words_en WHERE word = ?", (word,))
        result = cursor.fetchone()
        return result is not None


def db_get_words_count():
    """Получить количество слов в базе"""
    with sqlite3.connect("db/material.db", timeout=DB_TIMEOUT) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM words_en")
        return cursor.fetchone()[0]


def db_get_words_by_theme(theme: str, limit: int = 10):
    """
    Получить слова из базы данных по теме
    Возвращает список слов в формате (word, transcription, translation)
    """
    # Маппинг тем из русского в английский
    theme_mapping = {
        "животные": [
            "cat",
            "dog",
            "bird",
            "fish",
            "rabbit",
            "lion",
            "elephant",
            "tiger",
            "bear",
            "horse",
        ],
        "цвета": [
            "red",
            "blue",
            "green",
            "yellow",
            "orange",
            "purple",
            "pink",
            "black",
            "white",
            "brown",
        ],
        "еда": [
            "apple",
            "banana",
            "milk",
            "bread",
            "juice",
            "water",
            "cake",
            "cookie",
            "cheese",
            "egg",
        ],
        "семья": [
            "mother",
            "father",
            "sister",
            "brother",
            "grandma",
            "grandpa",
            "baby",
            "uncle",
            "aunt",
            "cousin",
        ],
        "одежда": [
            "dress",
            "shirt",
            "pants",
            "shoes",
            "hat",
            "socks",
            "jacket",
            "coat",
            "skirt",
            "boots",
        ],
        "дом": [
            "house",
            "room",
            "bed",
            "table",
            "chair",
            "window",
            "door",
            "kitchen",
            "bathroom",
            "bedroom",
        ],
        "школа": [
            "book",
            "pen",
            "pencil",
            "teacher",
            "student",
            "classroom",
            "desk",
            "backpack",
            "paper",
            "notebook",
        ],
        "хобби": [
            "read",
            "draw",
            "sing",
            "dance",
            "play",
            "swim",
            "run",
            "jump",
            "walk",
            "ride",
        ],
        "погода": [
            "sun",
            "rain",
            "snow",
            "cloud",
            "wind",
            "hot",
            "cold",
            "warm",
            "cool",
            "sky",
        ],
        "игрушки": [
            "toy",
            "ball",
            "doll",
            "car",
            "bike",
            "puzzle",
            "blocks",
            "teddy",
            "robot",
            "game",
        ],
        "природа": [
            "tree",
            "flower",
            "grass",
            "moon",
            "star",
            "mountain",
            "river",
            "ocean",
            "forest",
            "garden",
        ],
        "транспорт": [
            "car",
            "bus",
            "train",
            "plane",
            "bike",
            "boat",
            "truck",
            "motorcycle",
            "taxi",
            "subway",
        ],
        "спорт": [
            "football",
            "basketball",
            "tennis",
            "swimming",
            "running",
            "cycling",
            "dancing",
            "gymnastics",
            "boxing",
            "yoga",
        ],
        "музыка": [
            "piano",
            "guitar",
            "drum",
            "violin",
            "song",
            "music",
            "dance",
            "sing",
            "concert",
            "band",
        ],
        "искусство": [
            "paint",
            "draw",
            "color",
            "picture",
            "art",
            "museum",
            "gallery",
            "artist",
            "brush",
            "canvas",
        ],
    }

    # Получаем список слов для темы
    words_list = theme_mapping.get(theme, [])

    if not words_list:
        return []

    # Создаем плейсхолдеры для SQL запроса
    placeholders = ",".join(["?" for _ in words_list])

    with sqlite3.connect("db/material.db", timeout=DB_TIMEOUT) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT word, transkription, perevod FROM words_en WHERE word IN ({placeholders}) LIMIT ?",
            (*words_list, limit),
        )
        results = cursor.fetchall()

        # Возвращаем только английские слова
        return [word for word, _, _ in results]


def db_get_words_with_details(theme: str, limit: int = 10):
    """
    Получить слова из базы данных по теме с детальной информацией
    Возвращает список словарей с полной информацией о словах
    """
    # Маппинг тем из русского в английский
    theme_mapping = {
        "животные": [
            "cat",
            "dog",
            "bird",
            "fish",
            "rabbit",
            "lion",
            "elephant",
            "tiger",
            "bear",
            "horse",
        ],
        "цвета": [
            "red",
            "blue",
            "green",
            "yellow",
            "orange",
            "purple",
            "pink",
            "black",
            "white",
            "brown",
        ],
        "еда": [
            "apple",
            "banana",
            "milk",
            "bread",
            "juice",
            "water",
            "cake",
            "cookie",
            "cheese",
            "egg",
        ],
        "семья": [
            "mother",
            "father",
            "sister",
            "brother",
            "grandma",
            "grandpa",
            "baby",
            "uncle",
            "aunt",
            "cousin",
        ],
        "одежда": [
            "dress",
            "shirt",
            "pants",
            "shoes",
            "hat",
            "socks",
            "jacket",
            "coat",
            "skirt",
            "boots",
        ],
        "дом": [
            "house",
            "room",
            "bed",
            "table",
            "chair",
            "window",
            "door",
            "kitchen",
            "bathroom",
            "bedroom",
        ],
        "школа": [
            "book",
            "pen",
            "pencil",
            "teacher",
            "student",
            "classroom",
            "desk",
            "backpack",
            "paper",
            "notebook",
        ],
        "хобби": [
            "read",
            "draw",
            "sing",
            "dance",
            "play",
            "swim",
            "run",
            "jump",
            "walk",
            "ride",
        ],
        "погода": [
            "sun",
            "rain",
            "snow",
            "cloud",
            "wind",
            "hot",
            "cold",
            "warm",
            "cool",
            "sky",
        ],
        "игрушки": [
            "toy",
            "ball",
            "doll",
            "car",
            "bike",
            "puzzle",
            "blocks",
            "teddy",
            "robot",
            "game",
        ],
        "природа": [
            "tree",
            "flower",
            "grass",
            "moon",
            "star",
            "mountain",
            "river",
            "ocean",
            "forest",
            "garden",
        ],
        "транспорт": [
            "car",
            "bus",
            "train",
            "plane",
            "bike",
            "boat",
            "truck",
            "motorcycle",
            "taxi",
            "subway",
        ],
        "спорт": [
            "football",
            "basketball",
            "tennis",
            "swimming",
            "running",
            "cycling",
            "dancing",
            "gymnastics",
            "boxing",
            "yoga",
        ],
        "музыка": [
            "piano",
            "guitar",
            "drum",
            "violin",
            "song",
            "music",
            "dance",
            "sing",
            "concert",
            "band",
        ],
        "искусство": [
            "paint",
            "draw",
            "color",
            "picture",
            "art",
            "museum",
            "gallery",
            "artist",
            "brush",
            "canvas",
        ],
    }

    # Получаем список слов для темы
    words_list = theme_mapping.get(theme, [])

    if not words_list:
        return []

    # Создаем плейсхолдеры для SQL запроса
    placeholders = ",".join(["?" for _ in words_list])

    with sqlite3.connect("db/material.db", timeout=DB_TIMEOUT) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT word, transkription, perevod FROM words_en WHERE word IN ({placeholders}) LIMIT ?",
            (*words_list, limit),
        )
        results = cursor.fetchall()

        # Возвращаем список словарей с детальной информацией
        return [
            {
                "word": word,
                "transcription": transcription,
                "translation": translation
            }
            for word, transcription, translation in results
        ]
