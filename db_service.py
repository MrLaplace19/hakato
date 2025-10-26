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


def db_create_lessons_table():
    """Создание таблицы для сохранения уроков"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_lessons(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            theme TEXT NOT NULL,
            age_group TEXT NOT NULL,
            duration INTEGER NOT NULL,
            lesson_plan TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT
        )
        """)
        conn.commit()


def db_save_lesson(title, theme, age_group, duration, lesson_plan, created_by=None):
    """Сохранение урока в базу данных"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO saved_lessons (title, theme, age_group, duration, lesson_plan, created_by) VALUES (?, ?, ?, ?, ?, ?)",
            (title, theme, age_group, duration, lesson_plan, created_by)
        )
        conn.commit()
        return cursor.lastrowid


def db_get_all_lessons():
    """Получить все сохраненные уроки"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, title, theme, age_group, duration, created_at, created_by FROM saved_lessons ORDER BY created_at DESC"
        )
        results = cursor.fetchall()
        
        lessons = []
        for row in results:
            lessons.append({
                "id": row[0],
                "title": row[1],
                "theme": row[2],
                "age_group": row[3],
                "duration": row[4],
                "created_at": row[5],
                "created_by": row[6]
            })
        return lessons


def db_get_lesson_by_id(lesson_id):
    """Получить план урока по ID"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT lesson_plan FROM saved_lessons WHERE id = ?",
            (lesson_id,)
        )
        result = cursor.fetchone()
        
        if result:
            return result[0]
        return None


def db_get_full_lesson_by_id(lesson_id):
    """Получить полную информацию об уроке по ID"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, title, theme, age_group, duration, lesson_plan, created_at, created_by FROM saved_lessons WHERE id = ?",
            (lesson_id,)
        )
        result = cursor.fetchone()
        
        if result:
            return {
                "id": result[0],
                "title": result[1],
                "theme": result[2],
                "age_group": result[3],
                "duration": result[4],
                "lesson_plan": result[5],
                "created_at": result[6],
                "created_by": result[7]
            }
        return None


def db_update_lesson(lesson_id, title, theme, age_group, duration, lesson_plan):
    """Обновить урок по ID"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE saved_lessons SET title = ?, theme = ?, age_group = ?, duration = ?, lesson_plan = ? WHERE id = ?",
            (title, theme, age_group, duration, lesson_plan, lesson_id)
        )
        conn.commit()


def db_delete_lesson(lesson_id):
    """Удалить урок по ID"""
    with sqlite3.connect("db/material.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM saved_lessons WHERE id = ?",
            (lesson_id,)
        )
        conn.commit()