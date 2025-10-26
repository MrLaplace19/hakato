from enum import Enum
from typing import List
from dataclasses import dataclass
import json


class EnglishLevel(Enum):
    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    UPPER_INTERMEDIATE = "upper-intermediate"


class AgeGroup(Enum):
    TODDLERS = "1-3"
    PRESCHOOL = "3-6"
    EARLY_SCHOOL = "6-9"
    MID_SCHOOL = "9-12"
    TEENS = "12-15"


class ActivityType(Enum):
    GAME = "game"
    SONG = "song"
    STORY = "story"
    DIALOGUE = "dialogue"
    CRAFT = "craft"
    VIDEO = "video"
    QUIZ = "quiz"
    MOVEMENT = "movement"


class LessonPhase(Enum):
    WARM_UP = "warm_up"
    INTRODUCTION = "introduction"
    PRACTICE = "practice"
    PRODUCTION = "production"
    WRAP_UP = "wrap_up"


@dataclass
class LessonActivity:
    name: str
    activity_type: ActivityType
    duration: int  # в минутах
    description: str
    materials: List[str]
    instructions: List[str]

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.activity_type.value,
            "duration": self.duration,
            "description": self.description,
            "materials": self.materials,
            "instructions": self.instructions,
        }


class Lesson:
    def __init__(
        self,
        title: str,
        theme: str,
        age_group: AgeGroup,
        en_level: EnglishLevel,
        duration: int,
        objectives: List[str],
        activities: List[LessonActivity],
        vocabulary: List[str] = None,
    ):
        self.title = title
        self.theme = theme
        self.age_group = age_group
        self.en_level = en_level
        self.duration = duration
        self.objectives = objectives
        self.activities = activities
        self.vocabulary = vocabulary or []

        self._validate()

    def _validate(self):
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Название урока не может быть пустым")

        if len(self.title) > 100:
            raise ValueError("Название урока слишком длинное")

        if (
            not isinstance(self.duration, int)
            or self.duration <= 0
            or self.duration > 120
        ):
            raise ValueError("Длительность должна быть от 1 до 120 минут")

        if not self.objectives:
            raise ValueError("Укажите цели урока")

        if not self.activities:
            raise ValueError("Добавьте активности для урока")

        # Проверяем, что суммарная длительность активностей соответствует длительности урока
        total_activity_time = sum(activity.duration for activity in self.activities)
        if total_activity_time != self.duration:
            raise ValueError(
                f"Суммарное время активностей ({total_activity_time} мин) не совпадает с длительностью урока ({self.duration} мин)"
            )

    def add_activity(self, activity: LessonActivity):
        self.activities.append(activity)

    def get_lesson_plan(self) -> str:
        plan = f"ПЛАН УРОКА: {self.title}\n"
        plan += f"Тема: {self.theme} | Возраст: {self.age_group.value} | Уровень: {self.en_level.value}\n"
        plan += f"Длительность: {self.duration} минут\n\n"
        plan += "Цели:\n"
        for i, objective in enumerate(self.objectives, 1):
            plan += f"{i}. {objective}\n"

        plan += "\nАктивности:\n"
        for i, activity in enumerate(self.activities, 1):
            plan += f"{i}. {activity.name} ({activity.duration} мин) - {activity.description}\n"

        if self.vocabulary:
            plan += f"\nСловарный запас: {', '.join(self.vocabulary)}\n"

        return plan

    def to_dict(self):
        return {
            "title": self.title,
            "theme": self.theme,
            "age_group": self.age_group.value,
            "en_level": self.en_level.value,
            "duration": self.duration,
            "objectives": self.objectives,
            "vocabulary": self.vocabulary,
            "activities": [activity.to_dict() for activity in self.activities],
        }

    def __str__(self):
        return self.get_lesson_plan()


class ConsoleLessonBuilder:
    def __init__(self):
        self.themes = ["животные", "цвета", "еда", "семья", "одежда", "дом", "школа", "хобби"]
        self.activity_templates = self._load_templates()
    
    def _load_templates(self):
        return {
            "warm_up": {
                "3-6": [
                    LessonActivity("Приветственная песня", ActivityType.SONG, 5,
                                 "Веселая песня с движениями", ["колонка"],
                                 ["Включить музыку", "Показать движения", "Петь вместе с детьми"])
                ],
                "6-9": [
                    LessonActivity("Вопрос-ответ", ActivityType.DIALOGUE, 5,
                                 "Быстрые вопросы о настроении и погоде", [],
                                 ["Задать вопрос 'How are you?'", "Дети отвечают", "Спросить о погоде"])
                ]
            },
            "vocabulary": {
                "животные": [
                    LessonActivity("Угадай животное", ActivityType.GAME, 10,
                                 "Дети угадывают животных по звукам и описанию", ["карточки животных"],
                                 ["Показать карточку", "Издать звук животного", "Дети угадывают название"])
                ],
                "цвета": [
                    LessonActivity("Охота за цветами", ActivityType.GAME, 10,
                                 "Найти предметы определенного цвета в комнате", [],
                                 ["Назвать цвет", "Дети находят предметы этого цвета", "Назвать предметы на английском"])
                ]
            }
        }
    
    def start(self):
        print("🚀 КОНСТРУКТОР УРОКОВ АНГЛИЙСКОГО ДЛЯ ДЕТЕЙ")
        print("=" * 50)
        
        while True:
            lesson = self._create_lesson_interactive()
            if lesson:
                lesson.display()
                
                save = input("\n💾 Сохранить этот урок? (д/н): ").lower()
                if save == 'д':
                    self._save_lesson(lesson)
                
                another = input("\n🔄 Создать еще один урок? (д/н): ").lower()
                if another != 'д':
                    print("👋 До свидания!")
                    break
    
    def _create_lesson_interactive(self):
        print("\n" + "="*50)
        print("Создание нового урока")
        print("="*50)
        
        # Выбор темы
        print("\n🎨 Выберите тему урока:")
        for i, theme in enumerate(self.themes, 1):
            print(f"  {i}. {theme}")
        
        try:
            theme_choice = int(input("Введите номер темы: ")) - 1
            theme = self.themes[theme_choice]
        except (ValueError, IndexError):
            print("❌ Неверный выбор темы!")
            return None
        
        # Выбор возрастной группы
        print("\n👶 Выберите возрастную группу:")
        age_groups = list(AgeGroup)
        for i, age_group in enumerate(age_groups, 1):
            print(f"  {i}. {age_group.value} лет - {age_group.name}")
        
        try:
            age_choice = int(input("Введите номер возрастной группы: ")) - 1
            age_group = age_groups[age_choice]
        except (ValueError, IndexError):
            print("❌ Неверный выбор возрастной группы!")
            return None
        
        # Выбор уровня
        print("\n⭐ Выберите уровень английского:")
        levels = list(EnglishLevel)
        for i, level in enumerate(levels, 1):
            print(f"  {i}. {level.value}")
        
        try:
            level_choice = int(input("Введите номер уровня: ")) - 1
            en_level = levels[level_choice]
        except (ValueError, IndexError):
            print("❌ Неверный выбор уровня!")
            return None
        
        # Длительность урока
        try:
            duration = int(input("\n⏱️  Введите длительность урока (в минутах, 30-60): "))
            if duration < 30 or duration > 60:
                print("⚠️  Длительность установлена 45 минут")
                duration = 45
        except ValueError:
            print("⚠️  Длительность установлена 45 минут")
            duration = 45
        
        # Создание урока
        return self._generate_lesson(theme, age_group, en_level, duration)
    
    def _generate_lesson(self, theme: str, age_group: AgeGroup, 
                        en_level: EnglishLevel, duration: int) -> Lesson:
        # Генерация названия
        title = f"Веселый урок: {theme}"
        
        # Цели урока
        objectives = self._generate_objectives(theme, en_level, age_group)
        
        # Словарный запас
        vocabulary = self._generate_vocabulary(theme, age_group)
        
        # Активности
        activities = self._generate_activities(theme, age_group, en_level, duration)
        
        return Lesson(title, theme, age_group, en_level, duration, objectives, activities, vocabulary)
    
    def _generate_objectives(self, theme: str, level: EnglishLevel, age_group: AgeGroup) -> List[str]:
        base_objectives = {
            "beginner": [
                "Познакомиться с базовой лексикой по теме",
                "Научиться произносить 5-7 новых слов",
                "Развить интерес к английскому через игры"
            ],
            "elementary": [
                "Расширить словарный запас по теме",
                "Научиться строить простые предложения", 
                "Потренировать аудирование и говорение"
            ],
            "intermediate": [
                "Закрепить лексику по теме",
                "Практиковать диалогическую речь",
                "Развить коммуникативные навыки"
            ]
        }
        
        return base_objectives.get(level.value, ["Развить языковые навыки"])
    
    def _generate_vocabulary(self, theme: str, age_group: AgeGroup) -> List[str]:
        vocabulary_bank = {
            "животные": ["cat", "dog", "bird", "fish", "rabbit", "lion", "elephant"],
            "цвета": ["red", "blue", "green", "yellow", "orange", "purple", "pink"],
            "еда": ["apple", "banana", "milk", "bread", "juice", "water", "cake"],
            "семья": ["mother", "father", "sister", "brother", "grandma", "grandpa"],
            "одежда": ["dress", "shirt", "pants", "shoes", "hat", "socks", "jacket"],
            "дом": ["house", "room", "bed", "table", "chair", "window", "door"],
            "школа": ["book", "pen", "pencil", "teacher", "student", "classroom", "desk"],
            "хобби": ["read", "draw", "sing", "dance", "play", "swim", "run"]
        }
        
        words = vocabulary_bank.get(theme, [])
        # Ограничиваем количество слов по возрасту
        word_limit = {"3-6": 4, "6-9": 6, "9-12": 8, "12-15": 10}
        return words[:word_limit.get(age_group.value, 5)]
    
    def _generate_activities(self, theme: str, age_group: AgeGroup, 
                           level: EnglishLevel, duration: int) -> List[LessonActivity]:
        activities = []
        
        # Разминка (5 минут)
        warm_up = self._create_warm_up(age_group)
        activities.append(warm_up)
        
        # Основная часть (оставшееся время минус 5 минут на завершение)
        main_duration = duration - 10
        main_activities = self._create_main_activities(theme, age_group, level, main_duration)
        activities.extend(main_activities)
        
        # Завершение (5 минут)
        wrap_up = LessonActivity(
            "Подведение итогов", 
            ActivityType.DIALOGUE, 
            5,
            "Повторение и закрепление изученного",
            [],
            ["Спросить что запомнилось", "Повторить ключевые слова", "Похвалить детей"]
        )
        activities.append(wrap_up)
        
        return activities
    
    def _create_warm_up(self, age_group: AgeGroup) -> LessonActivity:
        if age_group == AgeGroup.PRESCHOOL:
            return LessonActivity(
                "Веселая разминка", 
                ActivityType.SONG, 
                5,
                "Песня с движениями для настроя на урок",
                ["аудиозапись песни"],
                ["Включить музыку", "Показать движения", "Петь вместе с детьми"]
            )
        else:
            return LessonActivity(
                "Быстрые вопросы",
                ActivityType.DIALOGUE,
                5,
                "Вопрос-ответ для активизации речи",
                [],
                ["Задать простые вопросы", "Выслушать ответы", "Поправить при необходимости"]
            )
    
    def _create_main_activities(self, theme: str, age_group: AgeGroup, 
                              level: EnglishLevel, duration: int) -> List[LessonActivity]:
        activities = []
        
        # Активность на введение лексики (40% времени)
        vocab_duration = int(duration * 0.4)
        vocab_activity = LessonActivity(
            f"Изучаем {theme}",
            ActivityType.GAME,
            vocab_duration,
            f"Знакомство со словами по теме '{theme}' через игру",
            ["карточки", "изображения"],
            ["Показать карточки", "Произнести слова", "Повторить хором", "Сыграть в игру"]
        )
        activities.append(vocab_activity)
        
        # Практическая активность (60% времени)
        practice_duration = duration - vocab_duration
        practice_activity = LessonActivity(
            "Играем и запоминаем",
            ActivityType.GAME,
            practice_duration,
            "Закрепление материала через игровую деятельность",
            ["игровые материалы", "реквизит"],
            ["Объяснить правила", "Провести игру", "Поощрять использование английского", "Подвести итоги игры"]
        )
        activities.append(practice_activity)
        
        return activities
    
    def _save_lesson(self, lesson: Lesson):
        filename = f"{lesson.theme}_{lesson.age_group.value}_{lesson.en_level.value}.json"
        lesson_data = {
            "title": lesson.title,
            "theme": lesson.theme,
            "age_group": lesson.age_group.value,
            "en_level": lesson.en_level.value,
            "duration": lesson.duration,
            "objectives": lesson.objectives,
            "vocabulary": lesson.vocabulary,
            "activities": [
                {
                    "name": activity.name,
                    "type": activity.activity_type.value,
                    "duration": activity.duration,
                    "description": activity.description,
                    "materials": activity.materials,
                    "instructions": activity.instructions
                }
                for activity in lesson.activities
            ]
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(lesson_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Урок сохранен в файл: {filename}")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")