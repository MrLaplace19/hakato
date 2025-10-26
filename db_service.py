import sqlite3


def db_create_words():
    with sqlite3.connect("db/material.db") as conn:
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
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO words_en (word,transkription,perevod) VALUES (?, ?, ?)",
            (word, transkription, pervod),
        )
        conn.commit()


def db_insert_users(persona):
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (login,password,age,role) VALUES (?, ?, ?, ?)",
            (persona.login, persona.password, persona.age, persona.role),
        )
        conn.commit()


def db_get_user(login, password):
    """Получить пользователя по логину и паролю"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT login, password, age, role FROM users WHERE login = ? AND password = ?",
            (login, password)
        )
        result = cursor.fetchone()
        
        if result:
            return {
                "login": result[0],
                "password": result[1],
                "age": result[2],
                "role": result[3]
            }
        return None


def db_check_user_exists(login):
    """Проверить существует ли пользователь с данным логином"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT login FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()
        return result is not None


def db_insert_user_simple(login, password, age, role):
    """Простая регистрация пользователя"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (login,password,age,role) VALUES (?, ?, ?, ?)",
            (login, password, age, role)
        )
        conn.commit()