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
    def _generate_lesson(self, theme, age_group, level, duration):
        return LessonPlan(
            theme=theme,
            age_group=age_group.value if hasattr(age_group, 'value') else age_group,
            level=level.value if hasattr(level, 'value') else level,
            duration=duration
        )

    def _get_vocabulary(self, theme, age_group):
        """Получить словарный запас для урока"""
        # Определяем лимит слов по возрасту
        word_limit = {"1-3": 3, "3-6": 4, "6-9": 6, "9-12": 8, "12-15": 10}
        age_value = age_group.value if hasattr(age_group, "value") else age_group
        limit = word_limit.get(age_value, 5)

        # Пытаемся получить слова из базы данных
        if self.db_get_words:
            try:
                words = self.db_get_words(theme, limit)
                if words:
                    return words
            except Exception:
                pass

        # Fallback словарь
        return []


class LessonPlan:
    def __init__(self, theme, age_group, level, duration, vocabulary=None):
        self.theme = theme
        self.age_group = age_group
        self.level = level
        self.duration = duration
        self.vocabulary = vocabulary or []

    def get_lesson_plan(self):
        phases = {
            45: [
                "Разминка (5 мин)",
                "Изучение лексики (15 мин)",
                "Игра (10 мин)",
                "Практика (10 мин)",
                "Завершение (5 мин)",
            ],
            60: [
                "Разминка (10 мин)",
                "Изучение лексики (20 мин)",
                "Игра (10 мин)",
                "Практика (15 мин)",
                "Завершение (5 мин)",
            ],
        }
        plan = f"🎓 ПЛАН УРОКА\n"
        plan += f"Тема: {self.theme.title()}\n"
        plan += f"Возраст: {self.age_group}\n"
        plan += f"Уровень: {self.level.upper()}\n"
        plan += f"Длительность: {self.duration} минут\n"
        plan += f"\nФАЗЫ УРОКА:\n"
        for phase in phases.get(self.duration, phases[45]):
            plan += f"• {phase}\n"

        # Добавляем словарь из базы данных
        if self.vocabulary:
            plan += f"\n📚 СЛОВАРНЫЙ ЗАПАС:\n"
            plan += f"• {', '.join(self.vocabulary)}\n"

        plan += f"\nМатериалы: карточки, аудио, раскраски по теме '{self.theme}'\n"
        return plan


# --- Конструктор занятий ---
def Constructor():
    win = tk.Toplevel()
    win.title("Конструктор уроков")
    win.geometry("1000x800")
    win.configure(bg="#f0f8ff")

    # Создаем главный фрейм с прокруткой
    main_canvas = tk.Canvas(win, bg="#f0f8ff")
    main_scrollbar = ttk.Scrollbar(win, orient="vertical", command=main_canvas.yview)
    scrollable_frame = tk.Frame(main_canvas, bg="#f0f8ff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
    )

    main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    main_canvas.configure(yscrollcommand=main_scrollbar.set)

    # Заголовок
    tk.Label(
        scrollable_frame,
        text="🎓 Конструктор уроков",
        font=("Arial", 24, "bold"),
        bg="#4169e1",
        fg="white",
        pady=15,
    ).pack(fill="x")

    # Основные параметры
    main_frame = tk.Frame(scrollable_frame, bg="#f0f8ff", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    # Тема
    tk.Label(frame, text="Тема урока:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, sticky="w", pady=10)
    theme_var = tk.StringVar(value="животные")
    ttk.Combobox(frame, textvariable=theme_var, values=["животные", "цвета", "еда", "семья", "одежда", "дом", "школа", "хобби"], width=30).grid(row=0, column=1)

    # Возраст
    tk.Label(frame, text="Возраст:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, sticky="w", pady=10)
    age_var = tk.StringVar(value="3-6")
    ttk.Combobox(frame, textvariable=age_var, values=["1-3", "3-6", "6-9", "9-12", "12-15"], width=30).grid(row=1, column=1)

    # Уровень
    tk.Label(frame, text="Уровень:", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, sticky="w", pady=10)
    level_var = tk.StringVar(value="beginner")
    ttk.Combobox(frame, textvariable=level_var, values=["beginner", "elementary", "intermediate", "upper-intermediate"], width=30).grid(row=2, column=1)

    # Длительность
    tk.Label(frame, text="Длительность (мин):", font=("Arial", 12), bg="#f0f8ff").grid(row=3, column=0, sticky="w", pady=10)
    duration_var = tk.StringVar(value="45")
    tk.Entry(frame, textvariable=duration_var, width=32).grid(row=3, column=1)

    # Область вывода
    tk.Label(frame, text="План урока:", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=5, column=0, columnspan=2, sticky="w", pady=10)
    output = scrolledtext.ScrolledText(frame, width=70, height=20, font=("Courier", 10))
    output.grid(row=6, column=0, columnspan=2, pady=10)

    def create_lesson():
        try:
            theme = theme_var.get().strip()
            age_str = age_var.get().strip()
            duration = int(duration_var.get())

            age_map = {"1-3": AgeGroup.TODDLERS, "3-6": AgeGroup.PRESCHOOL, "6-9": AgeGroup.EARLY_SCHOOL,
                       "9-12": AgeGroup.MID_SCHOOL, "12-15": AgeGroup.TEENS}
            level_map = {"beginner": EnglishLevel.BEGINNER, "elementary": EnglishLevel.ELEMENTARY,
                         "intermediate": EnglishLevel.INTERMEDIATE, "upper-intermediate": EnglishLevel.UPPER_INTERMEDIATE}

            if age_str not in age_map:
                raise ValueError("Неверная возрастная группа")

            lesson = ConsoleLessonBuilder()._generate_lesson(theme, age_map[age_str], level_map[level_str], duration)
            output.delete("1.0", tk.END)
            output.insert("1.0", lesson.get_lesson_plan())
            messagebox.showinfo("Готово", "Детальный урок успешно создан!")
        except ValueError as ve:
            messagebox.showerror("Ошибка", f"Некорректное значение: {ve}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    tk.Button(frame, text="Создать урок", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
              width=25, height=2, command=create_lesson).grid(row=4, column=0, columnspan=2, pady=20)


# --- Главное меню ---
def Menu():
    root = tk.Tk()
    root.title("Полиглотики — Главное меню")
    root.geometry("800x700")
    root.resizable(False, False)
    root.configure(bg="#f0f8ff")

    tk.Label(
        root,
        text="ПОЛИГЛОТИКИ",
        font=("Arial", 30, "bold"),
        bg="#4169e1",
        fg="white",
        pady=20,
    ).pack(fill="x")
    tk.Label(
        root,
        text="Детский языковой центр",
        font=("Arial", 16),
        bg="#f0f8ff",
        fg="#4169e1",
        pady=10,
    ).pack()

    tk.Label(
        root,
        text="Комплексное развитие: пение, танцы, рисование, творчество\n"
        "Задания на внимание, память, логику и мышление",
        font=("Arial", 12),
        bg="#f0f8ff",
        fg="#333333",
        pady=15,
        wraplength=650,
    ).pack()

    btn_frame = tk.Frame(root, bg="#f0f8ff")
    btn_frame.pack(pady=25)

    tk.Button(
        btn_frame,
        text="Игровые занятия\nдля дошкольников",
        font=("Arial", 14, "bold"),
        bg="#09d810",
        fg="black",
        width=20,
        height=3,
        command=lambda: messagebox.showinfo(
            "😊 Дошкольники", "Пение, танцы, игры на иностранном языке!"
        ),
    ).grid(row=0, column=0, padx=20)

    tk.Button(
        btn_frame,
        text="Клубы\nдля школьников",
        font=("Arial", 14, "bold"),
        bg="#0a8fe2",
        fg="black",
        width=20,
        height=3,
        command=lambda: messagebox.showinfo(
            "📘 Школьники", "Языковые клубы с проектами и играми!"
        ),
    ).grid(row=0, column=1, padx=20)

    # Центральная кнопка конструктора
    center_frame = tk.Frame(main_container, bg="#f0f8ff")
    center_frame.pack(pady=25)

    # Показываем кнопку конструктора только для учителей
    if current_user and current_user.get("role") == "учитель":
        tk.Button(
            center_frame,
            text="🛠️ Конструктор занятий",
            font=("Arial", 16, "bold"),
            bg="#FF9800",
            fg="white",
            width=25,
            height=2,
            command=Constructor,
        ).pack()

    tk.Label(
        root,
        text="Методика: One Person - One Language\nРазвиваем речь, восприятие, чтение, письмо",
        font=("Arial", 11),
        bg="#f0f8ff",
        fg="#555555",
        pady=15,
    ).pack()

    if current_user:
        username = current_user.get("login", "Пользователь")
        user_role = current_user.get("role", "")
        role_text = f" ({user_role})" if user_role else ""
        emoji = "👨‍🏫" if user_role == "учитель" else "🎓"
    else:
        username = "Пользователь"
        role_text = ""

    tk.Label(
        root,
        text=f"© 2025 Полиглотики — Добро пожаловать, {username}{role_text}!",
        font=("Arial", 10),
        bg="#f0f8ff",
        fg="#777",
    ).pack(side="bottom", pady=10)

    root.mainloop()


# --- Окно регистрации ---
def show_register_window(login_win, login_parent_entry=None):
    reg_win = tk.Toplevel()
    reg_win.title("Регистрация")
    reg_win.geometry("450x620")
    reg_win.resizable(False, False)
    
    # Красивый градиентный фон
    reg_win.configure(bg="#f0f8ff")

    tk.Label(
        reg_win,
        text="Создайте аккаунт",
        font=("Arial", 20, "bold"),
        bg="#f0f8ff",
        fg="#4169e1",
    ).pack(pady=20)

    tk.Label(reg_win, text="Логин:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
    login_entry = tk.Entry(reg_win, width=30)
    login_entry.pack()

    tk.Label(reg_win, text="Пароль:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
    password_entry = tk.Entry(reg_win, show="*", width=30)
    password_entry.pack()

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

    tk.Radiobutton(
        reg_win,
        text="Ученик",
        variable=role_var,
        value="ученик",
        bg="#f0f8ff",
        font=("Arial", 11),
    ).pack()
    tk.Radiobutton(
        reg_win,
        text="Учитель",
        variable=role_var,
        value="учитель",
        bg="#f0f8ff",
        font=("Arial", 11),
    ).pack()

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

        # Проверяем через БД
        if db_service.db_check_user_exists(login):
            messagebox.showwarning("Ошибка", "Логин уже занят.")
            return

        # Добавляем пользователя в БД
        db_service.db_insert_user_simple(login, password, age, role)

        messagebox.showinfo(
            "Успех", "Вы успешно зарегистрированы! Теперь войдите в систему."
        )
        reg_win.destroy()

        # Автозаполняем логин в окне входа
        if login_parent_entry:
            login_parent_entry.delete(0, tk.END)
            login_parent_entry.insert(0, login)

    tk.Button(
        reg_win,
        text="Зарегистрироваться",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        command=submit,
    ).pack(pady=20)


# --- Окно входа ---
def show_login_window():
    win = tk.Tk()
    win.title("Вход в Полиглотики")
    win.geometry("420x500")
    win.resizable(False, False)
    win.configure(bg="#f0f8ff")

    tk.Label(
        win,
        text="Добро пожаловать!",
        font=("Arial", 24, "bold"),
        bg="#f0f8ff",
        fg="#4169e1",
    ).pack(pady=20)

    tk.Label(win, text="Логин:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
    login_entry = tk.Entry(win, width=30)
    login_entry.pack()

    tk.Label(win, text="Пароль:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
    password_entry = tk.Entry(win, show="*", width=30)
    password_entry.pack()

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

    tk.Button(
        win,
        text="Войти",
        font=("Arial", 14, "bold"),
        bg="#4169e1",
        fg="white",
        width=15,
        command=login,
    ).pack(pady=20)

    link = tk.Label(
        win,
        text="Нет аккаунта? Зарегистрироваться",
        font=("Arial", 10, "underline"),
        bg="#f0f8ff",
        fg="#1e90ff",
        cursor="hand2",
    )
    link.pack(pady=10)
    link.bind("<Button-1>", lambda e: show_register_window(win, login_entry))

    win.mainloop()
