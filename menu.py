import tkinter as tk
from tkinter import messagebox

def show_kindergarten_activities():
    messagebox.showinfo("Игровые занятия", "Выбраны игровые занятия для дошкольников 3-7 лет. В программе: пение, танцы, рисование и творчество на иностранном языке.")

def show_school_clubs():
    messagebox.showinfo("Клубы для школьников", "Выбраны языковые клубы для школьников 1-6 классов. Программа включает изучение английского с использованием методики, учитывающей фонетические и грамматические особенности языков.")

def show_learning_materials():
    messagebox.showinfo("Учебные материалы", "Переход к записям учебных материалов. На платформе Полиглотики ваш ребенок может изучать иностранные языки с помощью уникальной методики, позволяющей овладеть языком за 3-6 месяцев.")

def Menu():
    # Создание главного окна
    root = tk.Tk()
    root.title("Меню Полиглотики")
    root.geometry("700x500")
    root.configure(bg="#f0f8ff")

    # Заголовок проекта
    header = tk.Label(root, text="ПОЛИГЛОТИКИ", font=("Arial", 28, "bold"), bg="#4169e1", fg="white", pady=20)
    header.pack(fill="x")
    
    subtitle = tk.Label(root, text="Детский языковой центр", font=("Arial", 16), bg="#f0f8ff", fg="#4169e1", pady=10)
    subtitle.pack()

    # Описание
    description = tk.Label(root, 
                          text="Комплексное развитие: пение, танцы, рисование, творчество\nЗадания на внимание, память, логику и мышление",
                          font=("Arial", 12), 
                          bg="#f0f8ff", 
                          fg="#333333",
                          pady=15,
                          wraplength=600)
    description.pack()

    # Фрейм для первых двух кнопок
    buttons_frame = tk.Frame(root, bg="#f0f8ff")
    buttons_frame.pack(pady=30)

    # Кнопки для дошкольников и школьников в одной строке
    kindergarten_button = tk.Button(buttons_frame, 
                                  text="Игровые занятия\nдля дошкольников", 
                                  font=("Arial", 14, "bold"),
                                  bg="#09d810", 
                                  fg="black", 
                                  width=20, 
                                  height=3,
                                  command=show_kindergarten_activities,
                                  relief="raised",
                                  borderwidth=3)
    kindergarten_button.grid(row=0, column=0, padx=20)

    school_button = tk.Button(buttons_frame, 
                             text="Клубы\nдля школьников", 
                             font=("Arial", 14, "bold"),
                             bg="#0a8fe2", 
                             fg="black", 
                             width=20, 
                             height=3,
                             command=show_school_clubs,
                             relief="raised",
                             borderwidth=3)
    school_button.grid(row=0, column=1, padx=20)

    # Кнопка для учебных материалов
    materials_button = tk.Button(root, 
                               text="Запись учебных материалов", 
                               font=("Arial", 14, "bold"),
                               bg="#CB1212", 
                               fg="black", 
                               width=30, 
                               height=2,
                               command=show_learning_materials,
                               relief="raised",
                               borderwidth=3)
    materials_button.pack(pady=20)

    # Информация о методике
    method_info = tk.Label(root, 
                          text="Мы используем методику 'One Person - One Language'\nи комплексный подход в изучении языка: речь, восприятие на слух, чтение и письмо",
                          font=("Arial", 11), 
                          bg="#f0f8ff", 
                          fg="#555555",
                          pady=10,
                          wraplength=600)
    method_info.pack()

    # Запуск приложения
    root.mainloop()