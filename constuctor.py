import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import db_service

# --- Хранилище текущего пользователя ---
current_user = None


# --- Функция для центрирования окна ---
def center_window(window):
    """Центрирует окно на экране"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


# --- Классы для Конструктора уроков ---
class AgeGroup:
    TODDLERS = "1-3"
    PRESCHOOL = "4-7"
    SCHOOL_AGE = "8-15"


class ConsoleLessonBuilder:
    def _generate_lesson(self, theme, age_group, duration):
        return LessonPlan(
            theme=theme,
            age_group=age_group.value if hasattr(age_group, 'value') else age_group,
            level="beginner",  # Фиксированный уровень
            duration=duration
        )


class LessonPlan:
    def __init__(self, theme, age_group, level, duration):
        self.theme = theme
        self.age_group = age_group
        self.level = level
        self.duration = duration

    def get_lesson_plan(self):
        phases = {
            45: ["Разминка (5 мин)", "Изучение лексики (15 мин)", "Игра (10 мин)", "Практика (10 мин)", "Завершение (5 мин)"],
            60: ["Разминка (10 мин)", "Изучение лексики (20 мин)", "Игра (10 мин)", "Практика (15 мин)", "Завершение (5 мин)"]
        }
        plan = f"🎓 ПЛАН УРОКА\n"
        plan += f"Тема: {self.theme.title()}\n"
        plan += f"Возраст: {self.age_group}\n"
        plan += f"Уровень: {self.level.upper()}\n"
        plan += f"Длительность: {self.duration} минут\n"
        plan += f"\nФАЗЫ УРОКА:\n"
        for phase in phases.get(self.duration, phases[45]):
            plan += f"• {phase}\n"
        plan += f"\nМатериалы: карточки, аудио, раскраски по теме '{self.theme}'\n"
        return plan


# --- Конструктор занятий ---
def Constructor():
    win = tk.Toplevel()
    win.title("Конструктор уроков")
    win.geometry("800x700")
    win.configure(bg="#f0f8ff")

    tk.Label(win, text="🎓 Конструктор уроков", font=("Arial", 24, "bold"), bg="#4169e1", fg="white", pady=15).pack(fill="x")

    frame = tk.Frame(win, bg="#f0f8ff", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    # Возрастная группа (первая)
    tk.Label(frame, text="Возрастная группа:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, sticky="w", pady=10)
    age_var = tk.StringVar()
    age_combo = ttk.Combobox(frame, textvariable=age_var, values=["Дети 1-3 года", "Дошкольники 4-7 лет", "Школьники 8-15 лет"], width=30, state="readonly")
    age_combo.grid(row=0, column=1)

    # Тема урока (вторая, зависит от возраста)
    tk.Label(frame, text="Тема урока:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, sticky="w", pady=10)
    theme_var = tk.StringVar()
    theme_combo = ttk.Combobox(frame, textvariable=theme_var, width=30, state="readonly")
    theme_combo.grid(row=1, column=1)

    # Длительность (третья)
    tk.Label(frame, text="Длительность (мин):", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, sticky="w", pady=10)
    duration_var = tk.StringVar(value="45")
    duration_combo = ttk.Combobox(frame, textvariable=duration_var, values=["30", "45", "60", "90"], width=30, state="readonly")
    duration_combo.grid(row=2, column=1)

    # Область вывода
    tk.Label(frame, text="План урока:", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=4, column=0, columnspan=2, sticky="w", pady=10)
    output = scrolledtext.ScrolledText(frame, width=70, height=20, font=("Courier", 10))
    output.grid(row=5, column=0, columnspan=2, pady=10)

    # Словари тем для разных возрастных групп
    themes_by_age = {
        "Дети 1-3 года": ["животные", "цвета", "части тела", "еда", "игрушки", "семья", "звуки животных"],
        "Дошкольники 4-7 лет": ["животные", "цвета", "семья", "еда", "одежда", "дом", "транспорт", "природа", "погода", "игрушки", "цифры 1-10"],
        "Школьники 8-15 лет": ["животные", "семья", "еда", "одежда", "дом", "школа", "хобби", "спорт", "путешествия", "технологии", "окружающая среда", "карьера", "искусство", "музыка", "литература"]
    }

    def update_themes(*args):
        """Обновляет список тем в зависимости от выбранной возрастной группы"""
        selected_age = age_var.get()
        if selected_age in themes_by_age:
            theme_combo['values'] = themes_by_age[selected_age]
            theme_combo.set('')  # Очищаем выбор темы
            theme_combo['state'] = 'readonly'

    # Привязываем обновление тем к выбору возраста
    age_var.trace('w', update_themes)

    def create_lesson():
        try:
            theme = theme_var.get().strip()
            age_str = age_var.get().strip()
            duration = int(duration_var.get())

            if not theme:
                raise ValueError("Выберите тему урока")
            if not age_str:
                raise ValueError("Выберите возрастную группу")

            # Маппинг возрастов на константы
            age_map = {
                "Дети 1-3 года": AgeGroup.TODDLERS,
                "Дошкольники 4-7 лет": AgeGroup.PRESCHOOL, 
                "Школьники 8-15 лет": AgeGroup.SCHOOL_AGE
            }

            if age_str not in age_map:
                raise ValueError("Неверная возрастная группа")

            # Используем фиксированный уровень (beginner) для всех уроков
            lesson = ConsoleLessonBuilder()._generate_lesson(theme, age_map[age_str], duration)
            output.delete("1.0", tk.END)
            output.insert("1.0", lesson.get_lesson_plan())
            messagebox.showinfo("Готово", "Урок успешно создан!")
        except ValueError as ve:
            messagebox.showerror("Ошибка", f"Некорректное значение: {ve}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    tk.Button(frame, text="Создать урок", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
              width=25, height=2, command=create_lesson).grid(row=3, column=0, columnspan=2, pady=20)


# --- Окно игровых занятий для дошкольников ---
def show_preschool_activities_window(root_parent=None):
    # Закрываем родительское окно если оно есть
    if root_parent:
        root_parent.destroy()
    
    activities_win = tk.Tk()
    activities_win.title("Игровые занятия для дошкольников")
    activities_win.geometry("750x700")
    activities_win.resizable(False, False)
    activities_win.configure(bg="#f0f8ff")
    
    center_window(activities_win)
    
    # Заголовок
    header_frame = tk.Frame(activities_win, bg="#4CAF50", height=100)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="🎨 Игровые занятия для дошкольников", 
             font=("Arial", 20, "bold"), bg="#4CAF50", fg="white").pack(pady=25)
    
    # Контейнер для занятий
    container = tk.Frame(activities_win, bg="#f0f8ff", padx=30, pady=20)
    container.pack(fill="both", expand=True)
    
    # Описание
    desc_frame = tk.Frame(container, bg="#e8f5e9", relief="solid", bd=1, padx=15, pady=10)
    desc_frame.pack(fill="x", pady=(0, 15))
    tk.Label(desc_frame, text="Выберите увлекательное занятие для развития английского языка!",
             font=("Arial", 11), bg="#e8f5e9", fg="#333").pack()
    
    # Описание для каждого занятия
    activities = [
        {
            "title": "🦁 Веселые животные",
            "description": "Узнаём названия животных на английском через игру",
            "details": "• Карточки с животными\n• Звуки животных\n• Угадай животное\n• 15 минут"
        },
        {
            "title": "🎨 Цвета и формы",
            "description": "Изучаем цвета и формы через творчество",
            "details": "• Рисование и раскраски\n• Игра 'Найди цвет'\n• Лепка из пластилина\n• 20 минут"
        },
        {
            "title": "🎵 Семейная песенка",
            "description": "Поём и танцуем, изучая семью",
            "details": "• Песня 'Family Song'\n• Движения под музыку\n• Карточки с семьёй\n• 15 минут"
        },
        {
            "title": "🎭 Танцуем и учимся",
            "description": "Движения под музыку с изучением слов",
            "details": "• Танцы под песни\n• Повторение слов\n• Мимика и жесты\n• 20 минут"
        },
        {
            "title": "✏️ Творческое рисование",
            "description": "Рисуем и изучаем английский одновременно",
            "details": "• Рисование цифр и букв\n• Раскраски с английскими словами\n• Фантазийные рисунки\n• 25 минут"
        }
    ]
    
    # Функция для открытия занятия
    def open_activity(activity):
        activity_win = tk.Toplevel(activities_win)
        activity_win.title(activity["title"])
        activity_win.geometry("600x500")
        activity_win.resizable(False, False)
        activity_win.configure(bg="#f0f8ff")
        center_window(activity_win)
        
        # Заголовок занятия
        header = tk.Frame(activity_win, bg="#4CAF50", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=activity["title"], 
                font=("Arial", 18, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
        
        # Основной контент
        content = tk.Frame(activity_win, bg="#f0f8ff", padx=30, pady=20)
        content.pack(fill="both", expand=True)
        
        # Описание
        tk.Label(content, text="Описание занятия:", 
                font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#333").pack(anchor="w", pady=(0, 5))
        tk.Label(content, text=activity["description"], 
                font=("Arial", 11), bg="#f0f8ff", fg="#555").pack(anchor="w", pady=(0, 15))
        
        # Детали
        tk.Label(content, text="Что включено:", 
                font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#333").pack(anchor="w", pady=(0, 5))
        
        details_frame = tk.Frame(content, bg="#e8f5e9", relief="solid", bd=1, padx=15, pady=10)
        details_frame.pack(fill="x", pady=(0, 15))
        tk.Label(details_frame, text=activity["details"], 
                font=("Arial", 11), bg="#e8f5e9", fg="#333", justify="left").pack(anchor="w")
        
        # Кнопка закрыть
        tk.Button(content, text="✅ Закрыть", font=("Arial", 12, "bold"),
                  bg="#4CAF50", fg="white", width=15, height=2,
                  activebackground="#45a049", relief="flat", bd=0,
                  command=activity_win.destroy).pack(pady=20)
    
    # Создаём кнопки для каждого занятия
    for i, activity in enumerate(activities):
        btn_frame = tk.Frame(container, bg="#f0f8ff")
        btn_frame.pack(pady=10, fill="x")
        
        btn = tk.Button(btn_frame, text=f"{activity['title']}\n\n{activity['description']}",
                        font=("Arial", 12, "bold"), bg="#66bb6a", fg="white",
                        height=3, relief="flat", bd=0,
                        activebackground="#4caf50", cursor="hand2",
                        wraplength=650, justify="center", anchor="w",
                        command=lambda a=activity: open_activity(a))
        btn.pack(padx=10, pady=5, fill="x")
    
    # Кнопка возврата
    back_frame = tk.Frame(container, bg="#f0f8ff")
    back_frame.pack(pady=20)
    
    def back_to_menu():
        activities_win.destroy()
        Menu()
    
    tk.Button(back_frame, text="🔙 Назад в главное меню", 
              font=("Arial", 11, "bold"), bg="#999999", fg="white",
              width=30, height=2, relief="flat", bd=0,
              activebackground="#777777",
              command=back_to_menu).pack()
    
    activities_win.mainloop()


# --- Окно клубов для школьников ---
def show_school_clubs_window(root_parent=None):
    # Закрываем родительское окно если оно есть
    if root_parent:
        root_parent.destroy()
    
    clubs_win = tk.Tk()
    clubs_win.title("Клубы для школьников")
    clubs_win.geometry("750x700")
    clubs_win.resizable(False, False)
    clubs_win.configure(bg="#f0f8ff")
    
    center_window(clubs_win)
    
    # Заголовок
    header_frame = tk.Frame(clubs_win, bg="#2196F3", height=100)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="🏫 Языковые клубы для школьников", 
             font=("Arial", 20, "bold"), bg="#2196F3", fg="white").pack(pady=25)
    
    # Контейнер для клубов
    container = tk.Frame(clubs_win, bg="#f0f8ff", padx=30, pady=20)
    container.pack(fill="both", expand=True)
    
    # Описание
    desc_frame = tk.Frame(container, bg="#e3f2fd", relief="solid", bd=1, padx=15, pady=10)
    desc_frame.pack(fill="x", pady=(0, 15))
    tk.Label(desc_frame, text="Выберите увлекательный клуб для развития английского языка!",
             font=("Arial", 11), bg="#e3f2fd", fg="#333").pack()
    
    # Описание для каждого клуба
    clubs = [
        {
            "title": "🌟 Project X - Приключения на английском",
            "description": "Читаем захватывающие истории и обсуждаем приключения",
            "details": "• Уровень: Beginner – Elementary (A1–A2)\n• Возраст: 1–4 классы\n• Чтение захватывающих историй\n• Создание комиксов и карт\n• Ролевые игры\n• 60–90 минут"
        },
        {
            "title": "🔍 English Detectives - Клуб юных следопытов",
            "description": "Увлекательные расследования и поиск улик на английском",
            "details": "• Уровень: Elementary – Pre-Intermediate (A2–B1)\n• Возраст: 3–6 классы\n• Поиск улик и подсказок\n• Интервью с подозреваемыми\n• Написание рапортов\n• Критическое мышление"
        },
        {
            "title": "✍️ Little Storymakers - Клуб писателей",
            "description": "Создаём свои книги и сочиняем истории на английском",
            "details": "• Уровень: Elementary+\n• Возраст: 4–6 классы\n• Написание рассказов\n• Оформление книг\n• Выставка авторов\n• Развитие письма"
        },
        {
            "title": "🌍 Global Kids - Клуб культур и путешествий",
            "description": "Изучаем культуру разных стран на английском",
            "details": "• Уровень: Все уровни\n• Возраст: 1–6 классы\n• Изучение стран и культур\n• Кулинарные мастер-классы\n• Празднование традиций\n• Носитель языка"
        },
        {
            "title": "🎭 Stage Time! - Театральный клуб",
            "description": "Ставим спектакли и развиваем уверенность в речи",
            "details": "• Уровень: Elementary и выше\n• Возраст: 3–6 классы\n• Постановка спектаклей\n• Разучивание ролей\n• Премьера для родителей\n• Развитие беглости"
        }
    ]
    
    # Функция для открытия клуба
    def open_club(club):
        club_win = tk.Toplevel(clubs_win)
        club_win.title(club["title"])
        club_win.geometry("600x550")
        club_win.resizable(False, False)
        club_win.configure(bg="#f0f8ff")
        center_window(club_win)
        
        # Заголовок клуба
        header = tk.Frame(club_win, bg="#2196F3", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=club["title"], 
                font=("Arial", 16, "bold"), bg="#2196F3", fg="white", wraplength=500).pack(pady=20)
        
        # Основной контент
        content = tk.Frame(club_win, bg="#f0f8ff", padx=30, pady=20)
        content.pack(fill="both", expand=True)
        
        # Описание
        tk.Label(content, text="Описание клуба:", 
                font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#333").pack(anchor="w", pady=(0, 5))
        tk.Label(content, text=club["description"], 
                font=("Arial", 11), bg="#f0f8ff", fg="#555").pack(anchor="w", pady=(0, 15))
        
        # Детали
        tk.Label(content, text="Что включает:", 
                font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#333").pack(anchor="w", pady=(0, 5))
        
        details_frame = tk.Frame(content, bg="#e3f2fd", relief="solid", bd=1, padx=15, pady=10)
        details_frame.pack(fill="x", pady=(0, 15))
        tk.Label(details_frame, text=club["details"], 
                font=("Arial", 11), bg="#e3f2fd", fg="#333", justify="left").pack(anchor="w")
        
        # Кнопка закрыть
        tk.Button(content, text="✅ Закрыть", font=("Arial", 12, "bold"),
                  bg="#2196F3", fg="white", width=15, height=2,
                  activebackground="#1976D2", relief="flat", bd=0,
                  command=club_win.destroy).pack(pady=20)
    
    # Создаём кнопки для каждого клуба
    for i, club in enumerate(clubs):
        btn_frame = tk.Frame(container, bg="#f0f8ff")
        btn_frame.pack(pady=10, fill="x")
        
        btn = tk.Button(btn_frame, text=f"{club['title']}\n\n{club['description']}",
                        font=("Arial", 11, "bold"), bg="#64b5f6", fg="white",
                        height=3, relief="flat", bd=0,
                        activebackground="#42a5f5", cursor="hand2",
                        wraplength=650, justify="left", anchor="w",
                        command=lambda c=club: open_club(c))
        btn.pack(padx=10, pady=5, fill="x")
    
    # Кнопка возврата
    back_frame = tk.Frame(container, bg="#f0f8ff")
    back_frame.pack(pady=20)
    
    def back_to_menu():
        clubs_win.destroy()
        Menu()
    
    tk.Button(back_frame, text="🔙 Назад в главное меню", 
              font=("Arial", 11, "bold"), bg="#999999", fg="white",
              width=30, height=2, relief="flat", bd=0,
              activebackground="#777777",
              command=back_to_menu).pack()
    
    clubs_win.mainloop()


# --- Главное меню ---
def Menu():
    root = tk.Tk()
    root.title("Полиглотики — Главное меню")
    root.geometry("800x700")
    root.resizable(False, False)
    root.configure(bg="#f0f8ff")

    # Центрируем окно
    center_window(root)

    # Красивый заголовок с градиентом
    header_frame = tk.Frame(root, bg="#4169e1", height=120)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="🎓 ПОЛИГЛОТИКИ", 
             font=("Arial", 32, "bold"), bg="#4169e1", fg="white").pack(pady=(20, 5))
    tk.Label(header_frame, text="Детский языковой центр", 
             font=("Arial", 16), bg="#4169e1", fg="white").pack(pady=(0, 20))

    # Основной контейнер
    main_container = tk.Frame(root, bg="#f0f8ff", padx=30, pady=20)
    main_container.pack(fill="both", expand=True)

    # Описание
    desc_frame = tk.Frame(main_container, bg="#e3f2fd", relief="solid", bd=1, padx=20, pady=15)
    desc_frame.pack(fill="x", pady=15)
    
    tk.Label(desc_frame,
             text="Комплексное развитие: пение, танцы, рисование, творчество\n"
                  "Задания на внимание, память, логику и мышление",
             font=("Arial", 12), bg="#e3f2fd", fg="#333", wraplength=650).pack()

    # Кнопки занятий
    btn_frame = tk.Frame(main_container, bg="#f0f8ff")
    btn_frame.pack(pady=20)
    
    # Получаем возраст пользователя
    user_age = None
    if current_user:
        user_age = current_user.get("age")
    
    # Функция для проверки доступа к дошкольным занятиям (доступны <= 7 лет)
    def check_preschool_access():
        if user_age is not None and user_age > 7:
            year_word = "лет" if user_age > 4 else ("год" if user_age == 1 else "года")
            messagebox.showinfo("⛔ Недоступно", 
                               f"🎨 Игровые занятия для дошкольников доступны только до 7 лет включительно.\n\n"
                               f"Ваш возраст: {user_age} {year_word}.\n\n"
                               f"📚 Для вас доступны клубы для школьников!\n"
                               f"Увлекательные проекты и продвинутые занятия ждут!")
        else:
            show_preschool_activities_window(root)
    
    # Функция для проверки доступа к клубам (доступны >= 7 лет)
    def check_club_access():
        if user_age is not None and user_age < 7:
            year_word = "лет" if user_age > 4 else ("год" if user_age == 1 else "года")
            messagebox.showinfo("⛔ Недоступно", 
                               f"📚 Клубы для школьников доступны только с 7 лет.\n\n"
                               f"Ваш возраст: {user_age} {year_word}.\n\n"
                               f"🎯 Изучайте материал для дошкольников!\n"
                               f"Увлекательные игры и занятия уже доступны!")
        else:
            show_school_clubs_window(root)

    # Создаем кнопку дошкольных занятий - меняем стиль если недоступна (недоступна > 7)
    if user_age is not None and user_age > 7:
        tk.Button(btn_frame, text="🎨 Игровые занятия\nдля дошкольников", 
                  font=("Arial", 14, "bold"), bg="#999999", fg="white", 
                  width=22, height=3, relief="flat", bd=0,
                  activebackground="#777777", cursor="hand2",
                  command=check_preschool_access).grid(row=0, column=0, padx=15)
        
        # Добавляем метку "Недоступно"
        tk.Label(btn_frame, text="👶 До 7 лет", 
                font=("Arial", 10, "italic"), bg="#f0f8ff", fg="#999").grid(row=1, column=0, pady=5)
    else:
        tk.Button(btn_frame, text="🎨 Игровые занятия\nдля дошкольников", 
                  font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                  width=22, height=3, relief="flat", bd=0,
                  activebackground="#45a049", cursor="hand2",
                  command=check_preschool_access).grid(row=0, column=0, padx=15)

    # Создаем кнопку клубов - меняем стиль если недоступна (недоступна < 7)
    if user_age is not None and user_age < 7:
        tk.Button(btn_frame, text="📚 Клубы\nдля школьников", 
                  font=("Arial", 14, "bold"), bg="#999999", fg="white", 
                  width=22, height=3, relief="flat", bd=0,
                  activebackground="#777777", cursor="hand2",
                  command=check_club_access).grid(row=0, column=1, padx=15)
        
        # Добавляем метку "Недоступно"
        tk.Label(btn_frame, text="⏳ Доступно с 7 лет", 
                font=("Arial", 10, "italic"), bg="#f0f8ff", fg="#999").grid(row=1, column=1, pady=5)
    else:
        tk.Button(btn_frame, text="📚 Клубы\nдля школьников", 
                  font=("Arial", 14, "bold"), bg="#2196F3", fg="white", 
                  width=22, height=3, relief="flat", bd=0,
                  activebackground="#0b7dda", cursor="hand2",
                  command=check_club_access).grid(row=0, column=1, padx=15)

    # Центральная кнопка конструктора
    center_frame = tk.Frame(main_container, bg="#f0f8ff")
    center_frame.pack(pady=25)

    # Показываем кнопку конструктора только для учителей
    if current_user and current_user.get("role") == "учитель":
        tk.Button(center_frame, text="🛠️ Конструктор занятий", 
                  font=("Arial", 16, "bold"), bg="#FF9800", fg="white", 
                  width=28, height=2, relief="flat", bd=0,
                  activebackground="#f57c00", cursor="hand2",
                  command=Constructor).pack()

    # Методика
    method_frame = tk.Frame(main_container, bg="#e3f2fd", relief="solid", bd=1, padx=20, pady=12)
    method_frame.pack(fill="x", pady=10)
    
    tk.Label(method_frame,
             text="📖 Методика: One Person - One Language\n💡 Развиваем речь, восприятие, чтение, письмо",
             font=("Arial", 11), bg="#e3f2fd", fg="#555555").pack()

    # Информация о пользователе внизу
    user_frame = tk.Frame(root, bg="#e8eaf6", height=50)
    user_frame.pack(fill="x", side="bottom")
    user_frame.pack_propagate(False)
    
    if current_user:
        username = current_user.get("login", "Пользователь")
        user_role = current_user.get("role", "")
        role_text = f" ({user_role})" if user_role else ""
        emoji = "👨‍🏫" if user_role == "учитель" else "🎓"
    else:
        username = "Пользователь"
        role_text = ""
        emoji = "👤"
    
    tk.Label(user_frame, text=f"{emoji} © 2025 Полиглотики — Добро пожаловать, {username}{role_text}!",
             font=("Arial", 11), bg="#e8eaf6", fg="#555").pack(pady=12)

    root.mainloop()


# --- Окно регистрации ---
def show_register_window(login_win, login_parent_entry=None):
    reg_win = tk.Toplevel()
    reg_win.title("Регистрация")
    reg_win.geometry("450x620")
    reg_win.resizable(False, False)
    
    # Красивый градиентный фон
    reg_win.configure(bg="#f0f8ff")

    # Центрируем окно
    center_window(reg_win)

    # Заголовок с иконкой
    header_frame = tk.Frame(reg_win, bg="#4169e1", height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="✏️ Создайте аккаунт", 
             font=("Arial", 22, "bold"), bg="#4169e1", fg="white").pack(pady=20)
    
    # Создаем контейнер для полей
    container = tk.Frame(reg_win, bg="#f0f8ff", padx=30, pady=20)
    container.pack(fill="both", expand=True)

    # Логин с иконкой
    login_frame = tk.Frame(container, bg="#f0f8ff")
    login_frame.pack(fill="x", pady=10)
    tk.Label(login_frame, text="👤 Логин:", font=("Arial", 11, "bold"), 
             bg="#f0f8ff", fg="#333").pack(anchor="w")
    login_entry = tk.Entry(login_frame, width=35, font=("Arial", 11), 
                          highlightthickness=2, relief="solid", bd=1)
    login_entry.config(highlightbackground="#ccc", highlightcolor="#4169e1")
    login_entry.pack(pady=5)
    
    # Пароль с иконкой
    password_frame = tk.Frame(container, bg="#f0f8ff")
    password_frame.pack(fill="x", pady=10)
    tk.Label(password_frame, text="🔒 Пароль:", font=("Arial", 11, "bold"), 
             bg="#f0f8ff", fg="#333").pack(anchor="w")
    password_entry = tk.Entry(password_frame, show="*", width=35, font=("Arial", 11),
                             highlightthickness=2, relief="solid", bd=1)
    password_entry.config(highlightbackground="#ccc", highlightcolor="#4169e1")
    password_entry.pack(pady=5)

    # Возраст с иконкой
    age_frame = tk.Frame(container, bg="#f0f8ff")
    age_frame.pack(fill="x", pady=10)
    tk.Label(age_frame, text="🎂 Возраст:", font=("Arial", 11, "bold"), 
             bg="#f0f8ff", fg="#333").pack(anchor="w")
    age_entry = tk.Entry(age_frame, width=35, font=("Arial", 11),
                        highlightthickness=2, relief="solid", bd=1)
    age_entry.config(highlightbackground="#ccc", highlightcolor="#4169e1")
    age_entry.pack(pady=5)

    # Роль с красивым дизайном
    role_frame = tk.Frame(container, bg="#f0f8ff")
    role_frame.pack(fill="x", pady=15)
    tk.Label(role_frame, text="👥 Выберите роль:", font=("Arial", 11, "bold"), 
             bg="#f0f8ff", fg="#333").pack(anchor="w", pady=(0, 8))
    
    role_var = tk.StringVar(value=None)

    # Стильные радиокнопки
    role_container = tk.Frame(role_frame, bg="#e3f2fd", relief="solid", bd=1)
    role_container.pack(fill="x", pady=5)
    
    tk.Radiobutton(role_container, text="🎓 Ученик", variable=role_var, value="ученик", 
                   bg="#e3f2fd", font=("Arial", 11), padx=20, pady=8,
                   selectcolor="#bbdefb", activebackground="#90caf9").pack(side="left", padx=10)
    
    tk.Radiobutton(role_container, text="👨‍🏫 Учитель", variable=role_var, value="учитель", 
                   bg="#e3f2fd", font=("Arial", 11), padx=20, pady=8,
                   selectcolor="#bbdefb", activebackground="#90caf9").pack(side="left", padx=10)

    def submit():
        global current_user
        login = login_entry.get().strip()
        password = password_entry.get().strip()
        age_str = age_entry.get().strip()
        role = role_var.get()

        if not login or not password or not age_str or not role:
            messagebox.showwarning("Ошибка", "Заполните все поля и выберите роль.")
            return
        if not age_str.isdigit() or not (1 <= int(age_str) <= 120):
            messagebox.showwarning("Ошибка", "Введите корректный возраст.")
            return
        
        age = int(age_str)
        
        # Проверка возраста для учеников
        if role == "ученик" and age > 14:
            messagebox.showwarning("Ошибка", 
                                 f"🎓 Ученики принимаются только до 14 лет (до 6 класса включительно).\n\n"
                                 f"Ваш возраст: {age} лет.\n\n"
                                 f"Для регистрации в качестве учителя выберите роль 'Учитель'.")
            return
        
        # Проверяем через БД
        if db_service.db_check_user_exists(login):
            messagebox.showwarning("Ошибка", "Логин уже занят.")
            return

        # Добавляем пользователя в БД
        db_service.db_insert_user_simple(login, password, age, role)

        messagebox.showinfo("Успех", "Вы успешно зарегистрированы! Теперь войдите в систему.")
        reg_win.destroy()
        
        # Автозаполняем логин в окне входа
        if login_parent_entry:
            login_parent_entry.delete(0, tk.END)
            login_parent_entry.insert(0, login)

    # Стильная кнопка регистрации
    tk.Button(container, text="✅ Зарегистрироваться", font=("Arial", 13, "bold"), 
              bg="#4CAF50", fg="white", width=25, height=2,
              activebackground="#45a049", activeforeground="white",
              relief="flat", bd=0, cursor="hand2",
              command=submit).pack(pady=20)
    
    # Фокус на первое поле
    login_entry.focus()


# --- Окно входа ---
def show_login_window():
    win = tk.Tk()
    win.title("Вход в Полиглотики")
    win.geometry("420x500")
    win.resizable(False, False)
    win.configure(bg="#f0f8ff")

    # Центрируем окно
    center_window(win)
    
    # Красивый заголовок
    header_frame = tk.Frame(win, bg="#4169e1", height=100)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="🎓 Добро пожаловать!", 
             font=("Arial", 26, "bold"), bg="#4169e1", fg="white").pack(pady=25)
    
    # Контейнер для полей
    container = tk.Frame(win, bg="#f0f8ff", padx=40, pady=30)
    container.pack(fill="both", expand=True)

    # Логин
    login_frame = tk.Frame(container, bg="#f0f8ff")
    login_frame.pack(fill="x", pady=15)
    tk.Label(login_frame, text="👤 Логин:", font=("Arial", 11, "bold"), 
             bg="#f0f8ff", fg="#333").pack(anchor="w")
    login_entry = tk.Entry(login_frame, width=35, font=("Arial", 11),
                          highlightthickness=2, relief="solid", bd=1)
    login_entry.config(highlightbackground="#ccc", highlightcolor="#4169e1")
    login_entry.pack(pady=5)

    # Пароль
    password_frame = tk.Frame(container, bg="#f0f8ff")
    password_frame.pack(fill="x", pady=15)
    tk.Label(password_frame, text="🔒 Пароль:", font=("Arial", 11, "bold"), 
             bg="#f0f8ff", fg="#333").pack(anchor="w")
    password_entry = tk.Entry(password_frame, show="*", width=35, font=("Arial", 11),
                             highlightthickness=2, relief="solid", bd=1)
    password_entry.config(highlightbackground="#ccc", highlightcolor="#4169e1")
    password_entry.pack(pady=5)

    def login():
        global current_user
        login = login_entry.get().strip()
        password = password_entry.get().strip()

        if not login or not password:
            messagebox.showwarning("Ошибка", "Введите логин и пароль.")
            return

        # Получаем пользователя из БД
        user = db_service.db_get_user(login, password)
        if user:
            current_user = user
            win.destroy()
            Menu()  # Переход в главное меню
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    # Кнопка входа
    tk.Button(container, text="🚪 Войти", font=("Arial", 13, "bold"), 
              bg="#4169e1", fg="white", width=20, height=2,
              activebackground="#2a56d1", activeforeground="white",
              relief="flat", bd=0, cursor="hand2",
              command=login).pack(pady=(0, 10))

    # Кнопка регистрации
    tk.Button(container, text="✨ Создать аккаунт", font=("Arial", 12, "bold"), 
              bg="#4CAF50", fg="white", width=20, height=2,
              activebackground="#45a049", activeforeground="white",
              relief="flat", bd=0, cursor="hand2",
              command=lambda: show_register_window(win, login_entry)).pack(pady=10)
    
    # Текст под кнопками
    tk.Label(container, text="Нет аккаунта? Нажмите кнопку выше", 
             font=("Arial", 10), bg="#f0f8ff", fg="#999").pack(pady=5)
    
    # Фокус на первое поле
    login_entry.focus()

    win.mainloop()

