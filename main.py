import sys
from base_c import ConsoleLessonBuilder, Person
from db_service import (
    db_create_words,
    db_insert_users,
    db_insert_word_en,
    db_insert_words_batch,
    db_check_word_exists,
    db_get_words_count,
)
from words_data import WORDS_LIST


def main():
    """
    Основная функция: запускает GUI-меню 'Полиглотики'.
    В будущем можно добавить поддержку --console для текстовой версии.
    """
    # Импортируем show_login_window для окна входа
    try:
        from constuctor import show_login_window

        show_login_window()  # Сначала показываем окно входа
    except ImportError as e:
        print("❌ Не удалось загрузить графическое меню.")
        print(f"   Ошибка импорта: {e}")
        print("   Убедитесь, что файл 'constuctor.py' находится в той же директории.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Произошла непредвиденная ошибка при запуске GUI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Инициализация базы данных и создание тестового пользователя
    from db_service import db_check_user_exists

    db_create_words()

    # Добавляем 100 слов в базу данных (если их ещё нет)
    words_to_add = []
    for word, transcription, translation in WORDS_LIST:
        if not db_check_word_exists(word):
            words_to_add.append((word, transcription, translation))

    if words_to_add:
        db_insert_words_batch(words_to_add)
        print(f"✅ Добавлено {len(words_to_add)} слов в базу данных")

    total_words = db_get_words_count()
    print(f"📚 Всего слов в базе данных: {total_words}")

    # Создаём тестового пользователя только если его ещё нет
    if not db_check_user_exists("admin"):
        persona = Person("admin", "admin123", 43, "учитель")
        db_insert_users(persona)
        print("✅ Тестовый пользователь создан: admin / admin123 (учитель)")

    # Создаём также тестового ученика для демонстрации
    if not db_check_user_exists("student"):
        persona_student = Person("student", "student123", 10, "ученик")
        db_insert_users(persona_student)
        print("✅ Тестовый ученик создан: student / student123")

    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        print("🎨 Запуск графического интерфейса 'Полиглотики'...")
        main()
    elif len(sys.argv) > 1 and sys.argv[1] == "--console":
        print("⌨️  Консольная версия.")
        print("🎉 Добро пожаловать в конструктор уроков английского для детей!")
        print(
            "   Этот инструмент поможет создать увлекательные уроки для разных возрастов.\n"
        )
        builder = ConsoleLessonBuilder()
        builder.start()
    else:
        # По умолчанию — запускаем GUI
        main()
