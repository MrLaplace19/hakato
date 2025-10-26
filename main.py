import sys
from base_c import ConsoleLessonBuilder, Person
from db_service import db_create_words, db_insert_users, db_insert_word_en


def main():
    print("🎉 Добро пожаловать в конструктор уроков английского для детей!")
    print(
        "   Этот инструмент поможет создать увлекательные уроки для разных возрастов.\n"
    )

    builder = ConsoleLessonBuilder()
    builder.start()


if __name__ == "__main__":
    persona = Person("admin", "admin123", 43, "Teacher")
    db_create_words()
    db_insert_word_en("theme", "teme", "тема")
    db_insert_users(persona)
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
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
        main()
