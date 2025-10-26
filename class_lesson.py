class Lesson:
    def __init__(self, title, theme, content, age_group, en_level, duration, task):
        self.title = title
        self.theme = theme
        self.content = content
        self.age_group = age_group
        self.en_level = en_level
        self.duration = duration
        self.task = task

        self._validate()

    def _validate(self):
        # Проверка title
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Название урока не может быть пустым")

        if len(self.title) > 100:
            raise ValueError("Название урока слишком длинное")

        # Проверка age_group (исправлено с target_age на age_group)
        if not isinstance(self.age_group, str) or "-" not in self.age_group:
            raise ValueError("Возраст должен быть в формате 'мин-макс'")

        try:
            min_age, max_age = map(int, self.age_group.split("-"))
            if min_age < 1 or max_age > 18 or min_age >= max_age:
                raise ValueError("Некорректный возрастной диапазон (1-18 лет)")
        except ValueError:
            raise ValueError("Возраст должен содержать числа в формате 'мин-макс'")

        # Проверка en_level (исправлено с level на en_level)
        valid_levels = [
            "beginner",
            "elementary",
            "intermediate",
            "upper-intermediate",
            "advanced",
        ]
        if self.en_level not in valid_levels:
            raise ValueError(f"Уровень должен быть одним из: {', '.join(valid_levels)}")

        # Проверка duration
        if (
            not isinstance(self.duration, int)
            or self.duration <= 0
            or self.duration > 180
        ):
            raise ValueError(
                "Длительность должна быть положительным числом (не более 180 минут)"
            )

        # Проверка task (исправлено с objectives на task)
        if not self.task or not isinstance(self.task, (list, str)):
            raise ValueError("Цели урока должны быть списком или строкой")

    def __str__(self):
        """Улучшенный вывод с переносами строк"""
        task_str = ", ".join(self.task) if isinstance(self.task, list) else self.task
        return (
            f"Название урока: {self.title}\n"
            f"Тема урока: {self.theme}\n"
            f"Содержание: {self.content}\n"
            f"Возрастная группа: {self.age_group}\n"
            f"Уровень владения английским: {self.en_level}\n"
            f"Время урока: {self.duration} мин\n"
            f"Цель урока: {task_str}"
        )

    def to_dict(self):
        """Дополнительный метод для преобразования в словарь (полезно для API)"""
        return {
            "title": self.title,
            "theme": self.theme,
            "content": self.content,
            "age_group": self.age_group,
            "en_level": self.en_level,
            "duration": self.duration,
            "task": self.task,
        }


class Group:
    def __init__(self, name, count, list_student):
        self.name = name
        self.count = count
        self.list_student = list_student
        self._validate()

    def _validate(self):
        """Валидация для группы"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Название группы не может быть пустым")

        if not isinstance(self.count, int) or self.count < 1:
            raise ValueError("Количество студентов должно быть положительным числом")

        if not isinstance(self.list_student, list):
            raise ValueError("Список студентов должен быть списком")

        if len(self.list_student) != self.count:
            raise ValueError("Количество студентов не соответствует длине списка")

    def __str__(self):
        """Улучшенный вывод для группы"""
        students_str = (
            ", ".join(self.list_student) if self.list_student else "нет студентов"
        )
        return (
            f"Название группы: {self.name}\n"
            f"Количество студентов: {self.count}\n"
            f"Студенты: {students_str}"
        )

    def add_student(self, student_name):
        """Метод для добавления студента"""
        if not student_name or not isinstance(student_name, str):
            raise ValueError("Имя студента должно быть непустой строкой")
        self.list_student.append(student_name)
        self.count += 1

    def remove_student(self, student_name):
        """Метод для удаления студента"""
        if student_name in self.list_student:
            self.list_student.remove(student_name)
            self.count -= 1
        else:
            raise ValueError(f"Студент {student_name} не найден в группе")

    def to_dict(self):
        """Преобразование в словарь"""
        return {
            "name": self.name,
            "count": self.count,
            "list_student": self.list_student,
        }
