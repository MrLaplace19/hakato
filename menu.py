import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from constuctor import ConsoleLessonBuilder, AgeGroup


def Menu():
    root = tk.Tk()
    root.title("Конструктор уроков английского")
    root.geometry("800x700")
    root.configure(bg="#f0f8ff")

    # Заголовок
    header = tk.Label(
        root,
        text="🎓 Конструктор уроков",
        font=("Arial", 24, "bold"),
        bg="#4169e1",
        fg="white",
        pady=15,
    )
    header.pack(fill="x")

    # Основной фрейм
    main_frame = tk.Frame(root, bg="#f0f8ff", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    # Тема
    tk.Label(main_frame, text="Тема урока:", font=("Arial", 12), bg="#f0f8ff").grid(
        row=0, column=0, sticky="w", pady=10
    )
    theme_var = tk.StringVar(value="животные")
    theme_combo = ttk.Combobox(
        main_frame,
        textvariable=theme_var,
        width=30,
        values=["животные", "цвета", "еда", "семья", "одежда", "дом", "школа", "хобби"],
    )
    theme_combo.grid(row=0, column=1, pady=10, padx=10)

    # Возрастная группа
    tk.Label(main_frame, text="Возраст:", font=("Arial", 12), bg="#f0f8ff").grid(
        row=1, column=0, sticky="w", pady=10
    )
    age_var = tk.StringVar(value="3-6")
    age_combo = ttk.Combobox(
        main_frame,
        textvariable=age_var,
        width=30,
        values=["1-3", "3-6", "6-9", "9-12", "12-15"],
    )
    age_combo.grid(row=1, column=1, pady=10, padx=10)

    # Уровень английского
    tk.Label(main_frame, text="Уровень:", font=("Arial", 12), bg="#f0f8ff").grid(
        row=2, column=0, sticky="w", pady=10
    )
    level_var = tk.StringVar(value="beginner")
    level_combo = ttk.Combobox(
        main_frame,
        textvariable=level_var,
        width=30,
        values=["beginner", "elementary", "intermediate", "upper-intermediate"],
    )
    level_combo.grid(row=2, column=1, pady=10, padx=10)

    # Длительность
    tk.Label(
        main_frame, text="Длительность (мин):", font=("Arial", 12), bg="#f0f8ff"
    ).grid(row=3, column=0, sticky="w", pady=10)
    duration_var = tk.StringVar(value="45")
    duration_entry = tk.Entry(main_frame, textvariable=duration_var, width=32)
    duration_entry.grid(row=3, column=1, pady=10, padx=10)

    # Кнопка создания
    create_btn = tk.Button(
        main_frame,
        text="Создать урок",
        font=("Arial", 14, "bold"),
        bg="#4CAF50",
        fg="white",
        width=25,
        height=2,
        command=lambda: create_lesson(),
    )
    create_btn.grid(row=4, column=0, columnspan=2, pady=20)

    # Область вывода результата
    tk.Label(
        main_frame, text="План урока:", font=("Arial", 12, "bold"), bg="#f0f8ff"
    ).grid(row=5, column=0, columnspan=2, sticky="w", pady=10)

    output_text = scrolledtext.ScrolledText(
        main_frame, width=70, height=20, font=("Courier", 10)
    )
    output_text.grid(row=6, column=0, columnspan=2, pady=10)

    def create_lesson():
        try:
            # Получаем параметры
            theme = theme_var.get()
            age_str = age_var.get()
            level_str = level_var.get()
            duration = int(duration_var.get())

            # Конвертируем в классы конструктора
            age_map = {
                "1-3": AgeGroup.TODDLERS,
                "4-7": AgeGroup.PRESCHOOL,
                "8-15": AgeGroup.SCHOOL_AGE,
            }
            age_group = age_map.get(age_str)
<<<<<<< HEAD
            en_level = level_map.get(level_str)

            if not age_group or not en_level:
                raise ValueError("Неверно выбран возраст или уровень")
=======
            
            if not age_group:
                raise ValueError("Неверно выбран возраст")
>>>>>>> origin/NIKITA

            # Создаем урок
            builder = ConsoleLessonBuilder()
            lesson = builder._generate_lesson(theme, age_group, duration)

            # Выводим результат
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", lesson.get_lesson_plan())

            # Показываем сообщение об успехе
            messagebox.showinfo("Успех", "Урок создан успешно!")

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверное значение: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    root.mainloop()
