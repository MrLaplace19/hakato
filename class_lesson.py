class lesson:
    def __init__(self, title, theme, content, age_group, en_level, duration, task):
        self.title = title  # Название урока
        self.content = content  # Содержание
        self.theme = theme  # Тема урока
        self.age_group = age_group  # Возраст группы
        self.en_level = en_level  # Уровень владения английским
        self.duration = duration  # Время урока
        self.task = task  # Цели урока

        self._validate()

    
    def _validate(self):
        
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Название урока не может быть пустым")
        
        if len(self.title) > 100:
            raise ValueError("Название урока слишком длинное")
        
        # Проверка target_age
        if not isinstance(self.target_age, str) or "-" not in self.target_age:
            raise ValueError("Возраст должен быть в формате 'мин-макс'")
        
        try:
            min_age, max_age = map(int, self.target_age.split("-"))
            if min_age < 1 or max_age > 18 or min_age >= max_age:
                raise ValueError("Некорректный возрастной диапазон")
        except ValueError:
            raise ValueError("Возраст должен содержать числа в формате 'мин-макс'")
        
        # Проверка level
        valid_levels = ["beginner", "elementary", "intermediate", "upper-intermediate", "advanced"]
        if self.level not in valid_levels:
            raise ValueError(f"Уровень должен быть одним из: {', '.join(valid_levels)}")
        
        # Проверка duration
        if not isinstance(self.duration, int) or self.duration <= 0 or self.duration > 180:
            raise ValueError("Длительность должна быть положительным числом (не более 180 минут)")
        
        # Проверка objectives
        if not self.objectives or not isinstance(self.objectives, list):
            raise ValueError("Цели урока должны быть списком")





    def printf(self):
        a = str(
            f"  Название уровка: {self.title}\
                    Тема урока: {self.theme}\
                    Содержание: {self.content}"
        )
        return a
