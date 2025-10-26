from base_c import *
from menu import menu


def main():
    print("🎉 Добро пожаловать в конструктор уроков английского для детей!")
    print("   Этот инструмент поможет создать увлекательные уроки для разных возрастов.\n")
    
    builder = ConsoleLessonBuilder()
    builder.start()


if __name__ == "__main__":
    menu()
    main()
