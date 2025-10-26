import sys


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
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        print("🎨 Запуск графического интерфейса 'Полиглотики'...")
        main()

    elif len(sys.argv) > 1 and sys.argv[1] == "--console":
        print("⌨️  Консольная версия пока временно недоступна. Запуск GUI по умолчанию.")
        main()  # Пока что тоже запускаем GUI, можно расширить позже

    else:
        # По умолчанию — запускаем GUI
        main()