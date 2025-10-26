import sys
<<<<<<< HEAD


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
=======
from base_c import ConsoleLessonBuilder, Person
from db_service import db_create_words, db_insert_users, db_insert_word_en


def main():
    print("🎉 Добро пожаловать в конструктор уроков английского для детей!")
    print(
        "   Этот инструмент поможет создать увлекательные уроки для разных возрастов.\n"
    )

    builder = ConsoleLessonBuilder()
    builder.start()
>>>>>>> d18c7eadb34d88b0f6601393e886d49fed917568


if __name__ == "__main__":
    persona = Person("admin", "admin123", 43, "Teacher")
    db_create_words()
    db_insert_word_en("theme", "teme", "тема")
    db_insert_users(persona)
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
<<<<<<< HEAD
        print("🎨 Запуск графического интерфейса 'Полиглотики'...")
=======
        # Запускаем GUI меню
        try:
            from menu import Menu

            Menu()
        except ImportError:
            print("❌ GUI недоступно. Требуется установить tkinter.")
            print("   Запустите: sudo apt-get install python3-tk")
            sys.exit(1)
    else:
        # Запускаем консольную версию
>>>>>>> d18c7eadb34d88b0f6601393e886d49fed917568
        main()

    elif len(sys.argv) > 1 and sys.argv[1] == "--console":
        print("⌨️  Консольная версия пока временно недоступна. Запуск GUI по умолчанию.")
        main()  # Пока что тоже запускаем GUI, можно расширить позже

    else:
        # По умолчанию — запускаем GUI
        main()