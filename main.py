import sys
from base_c import ConsoleLessonBuilder, Person
from db_service import db_create_words, db_insert_users, db_insert_word_en


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
    persona = Person("admin", "admin123", 43, "Teacher")
    db_create_words()
    db_insert_word_en("theme", "teme", "тема")
    db_insert_users(persona)
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        print("🎨 Запуск графического интерфейса 'Полиглотики'...")
        main()
    elif len(sys.argv) > 1 and sys.argv[1] == "--console":
        print("⌨️  Консольная версия.")
        print("🎉 Добро пожаловать в конструктор уроков английского для детей!")
        print("   Этот инструмент поможет создать увлекательные уроки для разных возрастов.\n")
        builder = ConsoleLessonBuilder()
        builder.start()
    else:
        # По умолчанию — запускаем GUI
        main()
