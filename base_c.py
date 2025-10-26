from enum import Enum
from typing import List
from dataclasses import dataclass
import json


class AgeGroup(Enum):
    TODDLERS = "1-3"
    PRESCHOOL = "4-7"
    SCHOOL_AGE = "8-15"


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
    learning_objectives: List[str] = None  # Цели конкретной активности
    difficulty_level: str = "medium"  # easy, medium, hard
    preparation_time: int = 5  # Время подготовки в минутах
    cleanup_time: int = 2  # Время уборки в минутах
    alternative_activities: List[str] = None  # Альтернативные активности
    assessment_criteria: List[str] = None  # Критерии оценки
    safety_notes: List[str] = None  # Меры безопасности
    technology_requirements: List[str] = None  # Технические требования

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.activity_type.value,
            "duration": self.duration,
            "description": self.description,
            "materials": self.materials,
            "instructions": self.instructions,
            "learning_objectives": self.learning_objectives or [],
            "difficulty_level": self.difficulty_level,
            "preparation_time": self.preparation_time,
            "cleanup_time": self.cleanup_time,
            "alternative_activities": self.alternative_activities or [],
            "assessment_criteria": self.assessment_criteria or [],
            "safety_notes": self.safety_notes or [],
            "technology_requirements": self.technology_requirements or [],
        }


class Lesson:
    def __init__(
        self,
        title: str,
        theme: str,
        age_group: AgeGroup,
        duration: int,
        objectives: List[str],
        activities: List[LessonActivity],
        vocabulary: List[str] = None,
        # Дополнительные поля
        lesson_phases: List[dict] = None,  # Детальные фазы урока
        materials_summary: List[str] = None,  # Общий список материалов
        assessment_methods: List[str] = None,  # Методы оценки
        homework_suggestions: List[str] = None,  # Предложения по домашнему заданию
        extension_activities: List[str] = None,  # Дополнительные активности
        cultural_notes: List[str] = None,  # Культурные заметки
        common_mistakes: List[str] = None,  # Частые ошибки
        teacher_notes: List[str] = None,  # Заметки для учителя
        student_handouts: List[str] = None,  # Раздаточные материалы
        technology_tools: List[str] = None,  # Технологические инструменты
        room_setup: str = "",  # Организация пространства
        group_size: str = "8-12",  # Размер группы
        prerequisites: List[str] = None,  # Предварительные знания
    ):
        self.title = title
        self.theme = theme
        self.age_group = age_group
        self.duration = duration
        self.objectives = objectives
        self.activities = activities
        self.vocabulary = vocabulary or []
        
        # Дополнительные поля
        self.lesson_phases = lesson_phases or []
        self.materials_summary = materials_summary or []
        self.assessment_methods = assessment_methods or []
        self.homework_suggestions = homework_suggestions or []
        self.extension_activities = extension_activities or []
        self.cultural_notes = cultural_notes or []
        self.common_mistakes = common_mistakes or []
        self.teacher_notes = teacher_notes or []
        self.student_handouts = student_handouts or []
        self.technology_tools = technology_tools or []
        self.room_setup = room_setup
        self.group_size = group_size
        self.prerequisites = prerequisites or []

        self._validate()

    def _validate(self):
        """Валидация урока с улучшенными проверками"""
        # Проверка названия
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Название урока не может быть пустым")

        if len(self.title) > 100:
            raise ValueError("Название урока слишком длинное (максимум 100 символов)")

        # Проверка длительности
        if not isinstance(self.duration, int):
            raise ValueError("Длительность должна быть целым числом")
        
        if self.duration <= 0:
            raise ValueError("Длительность должна быть положительным числом")
        
        if self.duration > 180:  # Увеличили лимит до 3 часов
            raise ValueError("Длительность не должна превышать 180 минут")

        # Проверка минимальной длительности в зависимости от возраста
        age_min_duration = {
            "1-3": 10,
            "3-6": 15,
            "6-9": 20,
            "9-12": 25,
            "12-15": 30
        }
        min_duration = age_min_duration.get(self.age_group.value, 15)
        if self.duration < min_duration:
            raise ValueError(f"Минимальная длительность для возраста {self.age_group.value} лет: {min_duration} минут")

        # Проверка целей урока
        if not self.objectives:
            raise ValueError("Укажите цели урока")

        if len(self.objectives) < 2:
            raise ValueError("Должно быть минимум 2 образовательные цели")

        if len(self.objectives) > 8:
            raise ValueError("Слишком много целей урока (максимум 8)")

        # Проверка активностей
        if not self.activities:
            raise ValueError("Добавьте активности для урока")

        if len(self.activities) < 2:
            raise ValueError("Должно быть минимум 2 активности")

        if len(self.activities) > 10:
            raise ValueError("Слишком много активностей (максимум 10)")

        # Проверка длительности активностей
        for i, activity in enumerate(self.activities, 1):
            if activity.duration <= 0:
                raise ValueError(f"Активность {i} должна иметь положительную длительность")
            
            if activity.duration > 60:
                raise ValueError(f"Активность {i} слишком длинная (максимум 60 минут)")

        # Проверка соответствия суммарного времени активностей длительности урока
        total_activity_time = sum(activity.duration for activity in self.activities)
        time_difference = abs(total_activity_time - self.duration)
        
        if time_difference > 5:  # Допускаем разницу до 5 минут
            raise ValueError(
                f"Суммарное время активностей ({total_activity_time} мин) значительно отличается от длительности урока ({self.duration} мин). "
                f"Разница: {time_difference} минут"
            )

        # Проверка словарного запаса
        if self.vocabulary:
            if isinstance(self.vocabulary[0], dict):
                # Проверяем структуру детального словаря
                for i, word_info in enumerate(self.vocabulary, 1):
                    if not isinstance(word_info, dict):
                        raise ValueError(f"Элемент словаря {i} должен быть словарем")
                    
                    required_keys = ["word", "transcription", "translation"]
                    for key in required_keys:
                        if key not in word_info:
                            raise ValueError(f"В элементе словаря {i} отсутствует ключ '{key}'")
                    
                    if not word_info["word"] or not word_info["word"].strip():
                        raise ValueError(f"Слово в элементе {i} не может быть пустым")
            else:
                # Проверяем простой список слов
                for i, word in enumerate(self.vocabulary, 1):
                    if not word or not str(word).strip():
                        raise ValueError(f"Слово {i} не может быть пустым")

        # Проверка разнообразия активностей
        activity_types = [activity.activity_type for activity in self.activities]
        if len(set(activity_types)) < 2:
            raise ValueError("Добавьте разнообразие в типы активностей")

        # Проверка логической последовательности активностей
        warm_up_keywords = ["разминка", "warm", "привет", "музыкальная", "быстрые", "вопрос"]
        warm_up_count = sum(1 for activity in self.activities 
                          if any(keyword in activity.name.lower() for keyword in warm_up_keywords))
        if warm_up_count == 0:
            # Не строгая ошибка, только предупреждение
            print("⚠️  Рекомендуется добавить разминочную активность в начало урока")

        wrap_up_keywords = ["завершение", "итог", "wrap", "прощание", "повторение", "рефлексия"]
        wrap_up_count = sum(1 for activity in self.activities 
                          if any(keyword in activity.name.lower() for keyword in wrap_up_keywords))
        if wrap_up_count == 0:
            # Не строгая ошибка, только предупреждение
            print("⚠️  Рекомендуется добавить завершающую активность в конец урока")

    def add_activity(self, activity: LessonActivity):
        self.activities.append(activity)

    def get_lesson_plan(self) -> str:
        plan = f"🎓 ПЛАН УРОКА: {self.title}\n"
        plan += "=" * 80 + "\n"
        plan += f"📚 Тема: {self.theme.title()}\n"
        plan += f"👶 Возрастная группа: {self.age_group.value} лет\n"
        plan += f"⭐ Уровень английского: {self.en_level.value.upper()}\n"
        plan += f"⏱️  Длительность: {self.duration} минут\n"
        plan += f"👥 Размер группы: {self.group_size} человек\n"
        plan += f"🏫 Организация пространства: {self.room_setup or 'Стандартная классная комната'}\n"
        plan += "=" * 80 + "\n\n"
        
        # Предварительные знания
        if self.prerequisites:
            plan += "📋 ПРЕДВАРИТЕЛЬНЫЕ ЗНАНИЯ:\n"
            for i, prereq in enumerate(self.prerequisites, 1):
                plan += f"   {i}. {prereq}\n"
            plan += "\n"

        # Образовательные цели
        plan += "🎯 ОБРАЗОВАТЕЛЬНЫЕ ЦЕЛИ:\n"
        for i, objective in enumerate(self.objectives, 1):
            plan += f"   {i}. {objective}\n"

        # Детальные фазы урока
        if self.lesson_phases:
            plan += "\n📅 ДЕТАЛЬНЫЕ ФАЗЫ УРОКА:\n"
            for i, phase in enumerate(self.lesson_phases, 1):
                plan += f"   {i}. {phase.get('name', 'Фаза')} ({phase.get('duration', 0)} мин)\n"
                plan += f"      📝 {phase.get('description', '')}\n"
                if phase.get('objectives'):
                    plan += f"      🎯 Цели: {', '.join(phase['objectives'])}\n"
                plan += "\n"

        # Структура урока с детальной информацией
        plan += "📋 ДЕТАЛЬНАЯ СТРУКТУРА УРОКА:\n"
        total_time = 0
        for i, activity in enumerate(self.activities, 1):
            plan += f"   {i}. {activity.name} ({activity.duration} мин)\n"
            plan += f"      📝 {activity.description}\n"
            plan += f"      🎯 Уровень сложности: {activity.difficulty_level.upper()}\n"
            plan += f"      ⏰ Подготовка: {activity.preparation_time} мин | Уборка: {activity.cleanup_time} мин\n"
            
            if activity.materials:
                plan += f"      🎨 Материалы: {', '.join(activity.materials)}\n"
            
            if activity.technology_requirements:
                plan += f"      💻 Техника: {', '.join(activity.technology_requirements)}\n"
            
            if activity.learning_objectives:
                plan += f"      🎯 Цели активности:\n"
                for obj in activity.learning_objectives:
                    plan += f"         • {obj}\n"
            
            plan += f"      📋 Пошаговые инструкции:\n"
            for j, instruction in enumerate(activity.instructions, 1):
                plan += f"         {j}. {instruction}\n"
            
            if activity.assessment_criteria:
                plan += f"      📊 Критерии оценки:\n"
                for criterion in activity.assessment_criteria:
                    plan += f"         • {criterion}\n"
            
            if activity.safety_notes:
                plan += f"      ⚠️  Меры безопасности:\n"
                for note in activity.safety_notes:
                    plan += f"         • {note}\n"
            
            if activity.alternative_activities:
                plan += f"      🔄 Альтернативные активности:\n"
                for alt in activity.alternative_activities:
                    plan += f"         • {alt}\n"
            
            plan += "\n"
            total_time += activity.duration

        # Словарный запас
        if self.vocabulary:
            plan += "📖 СЛОВАРНЫЙ ЗАПАС:\n"
            if isinstance(self.vocabulary[0], dict):
                # Детальная информация о словах
                for word_info in self.vocabulary:
                    plan += f"   • {word_info['word']} [{word_info['transcription']}] - {word_info['translation']}\n"
            else:
                # Простой список слов
                plan += f"   • {', '.join(self.vocabulary)}\n"

        # Общий список материалов
        if self.materials_summary:
            plan += "\n🎨 ОБЩИЙ СПИСОК МАТЕРИАЛОВ:\n"
            for i, material in enumerate(self.materials_summary, 1):
                plan += f"   {i}. {material}\n"

        # Технологические инструменты
        if self.technology_tools:
            plan += "\n💻 ТЕХНОЛОГИЧЕСКИЕ ИНСТРУМЕНТЫ:\n"
            for i, tool in enumerate(self.technology_tools, 1):
                plan += f"   {i}. {tool}\n"

        # Раздаточные материалы
        if self.student_handouts:
            plan += "\n📄 РАЗДАТОЧНЫЕ МАТЕРИАЛЫ:\n"
            for i, handout in enumerate(self.student_handouts, 1):
                plan += f"   {i}. {handout}\n"

        # Методы оценки
        if self.assessment_methods:
            plan += "\n📊 МЕТОДЫ ОЦЕНКИ:\n"
            for i, method in enumerate(self.assessment_methods, 1):
                plan += f"   {i}. {method}\n"

        # Домашнее задание
        if self.homework_suggestions:
            plan += "\n📚 ПРЕДЛОЖЕНИЯ ПО ДОМАШНЕМУ ЗАДАНИЮ:\n"
            for i, hw in enumerate(self.homework_suggestions, 1):
                plan += f"   {i}. {hw}\n"

        # Дополнительные активности
        if self.extension_activities:
            plan += "\n🔄 ДОПОЛНИТЕЛЬНЫЕ АКТИВНОСТИ:\n"
            for i, ext in enumerate(self.extension_activities, 1):
                plan += f"   {i}. {ext}\n"

        # Культурные заметки
        if self.cultural_notes:
            plan += "\n🌍 КУЛЬТУРНЫЕ ЗАМЕТКИ:\n"
            for i, note in enumerate(self.cultural_notes, 1):
                plan += f"   {i}. {note}\n"

        # Частые ошибки
        if self.common_mistakes:
            plan += "\n❌ ЧАСТЫЕ ОШИБКИ И КАК ИХ ИЗБЕЖАТЬ:\n"
            for i, mistake in enumerate(self.common_mistakes, 1):
                plan += f"   {i}. {mistake}\n"

        # Заметки для учителя
        if self.teacher_notes:
            plan += "\n👩‍🏫 ЗАМЕТКИ ДЛЯ УЧИТЕЛЯ:\n"
            for i, note in enumerate(self.teacher_notes, 1):
                plan += f"   {i}. {note}\n"

        plan += f"\n📊 ИТОГО ВРЕМЕНИ: {total_time} минут\n"
        plan += "=" * 80 + "\n"

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
            # Дополнительные поля
            "lesson_phases": self.lesson_phases,
            "materials_summary": self.materials_summary,
            "assessment_methods": self.assessment_methods,
            "homework_suggestions": self.homework_suggestions,
            "extension_activities": self.extension_activities,
            "cultural_notes": self.cultural_notes,
            "common_mistakes": self.common_mistakes,
            "teacher_notes": self.teacher_notes,
            "student_handouts": self.student_handouts,
            "technology_tools": self.technology_tools,
            "room_setup": self.room_setup,
            "group_size": self.group_size,
            "prerequisites": self.prerequisites,
        }

    def __str__(self):
        return self.get_lesson_plan()


class ConsoleLessonBuilder:
    def __init__(self):
        self.themes = [
            "животные",
            "цвета",
            "еда",
            "семья",
            "одежда",
            "дом",
            "школа",
            "хобби",
            "погода",
            "игрушки",
            "природа",
            "транспорт",
            "спорт",
            "музыка",
            "искусство"
        ]
        self.activity_templates = self._load_templates()
        self.learning_objectives = self._load_learning_objectives()
        self.lesson_templates = self._load_lesson_templates()
        # Импортируем функцию для работы с БД
        try:
            from db_service import db_get_words_by_theme

            self.db_get_words = db_get_words_by_theme
        except ImportError:
            self.db_get_words = None

    def _load_learning_objectives(self):
        """Загружает образовательные цели для разных комбинаций возраста и уровня"""
        return {
            "1-3": {
                "beginner": [
                    "Развить базовое понимание английских звуков",
                    "Научиться произносить 3-5 простых слов",
                    "Развить интерес к английскому языку через игру",
                    "Улучшить слуховое восприятие иностранной речи"
                ],
                "elementary": [
                    "Расширить словарный запас до 8-10 слов",
                    "Научиться понимать простые команды",
                    "Развить моторику через движения под музыку",
                    "Улучшить концентрацию внимания"
                ]
            },
            "3-6": {
                "beginner": [
                    "Изучить 5-7 новых слов по теме",
                    "Научиться произносить слова с правильной интонацией",
                    "Развить навыки аудирования",
                    "Улучшить память через повторение"
                ],
                "elementary": [
                    "Построить простые фразы из 2-3 слов",
                    "Научиться отвечать на простые вопросы",
                    "Развить творческие способности через рисование",
                    "Улучшить социальные навыки в группе"
                ],
                "intermediate": [
                    "Использовать изученную лексику в диалогах",
                    "Научиться описывать предметы простыми словами",
                    "Развить логическое мышление через игры",
                    "Улучшить координацию движений"
                ]
            },
            "6-9": {
                "beginner": [
                    "Изучить 8-10 новых слов с транскрипцией",
                    "Научиться читать простые слова",
                    "Развить навыки говорения",
                    "Улучшить произношение"
                ],
                "elementary": [
                    "Строить предложения из 4-5 слов",
                    "Научиться задавать вопросы",
                    "Развить навыки письма (печатные буквы)",
                    "Улучшить понимание грамматических структур"
                ],
                "intermediate": [
                    "Вести простые диалоги по теме",
                    "Научиться рассказывать короткие истории",
                    "Развить навыки чтения",
                    "Улучшить понимание на слух"
                ],
                "upper-intermediate": [
                    "Использовать сложные грамматические конструкции",
                    "Научиться выражать свое мнение",
                    "Развить навыки письма",
                    "Улучшить беглость речи"
                ]
            },
            "9-12": {
                "beginner": [
                    "Изучить 10-12 новых слов с правильным произношением",
                    "Научиться читать и понимать простые тексты",
                    "Развить навыки аудирования",
                    "Улучшить грамматические знания"
                ],
                "elementary": [
                    "Строить сложные предложения",
                    "Научиться вести дискуссии",
                    "Развить навыки письма",
                    "Улучшить понимание культурных особенностей"
                ],
                "intermediate": [
                    "Использовать идиомы и фразеологизмы",
                    "Научиться анализировать тексты",
                    "Развить навыки презентации",
                    "Улучшить критическое мышление"
                ],
                "upper-intermediate": [
                    "Вести дебаты на английском языке",
                    "Научиться писать эссе",
                    "Развить навыки перевода",
                    "Улучшить понимание нюансов языка"
                ]
            },
            "12-15": {
                "beginner": [
                    "Изучить 12-15 новых слов с контекстом",
                    "Научиться понимать быструю речь",
                    "Развить навыки письма",
                    "Улучшить грамматическую точность"
                ],
                "elementary": [
                    "Использовать сложную лексику",
                    "Научиться анализировать литературные тексты",
                    "Развить навыки исследовательской работы",
                    "Улучшить понимание академического языка"
                ],
                "intermediate": [
                    "Вести профессиональные дискуссии",
                    "Научиться писать научные работы",
                    "Развить навыки публичных выступлений",
                    "Улучшить понимание культурных различий"
                ],
                "upper-intermediate": [
                    "Достичь уровня носителя языка",
                    "Научиться преподавать английский",
                    "Развить навыки лингвистического анализа",
                    "Улучшить понимание региональных диалектов"
                ]
            }
        }

    def _load_templates(self):
        """Загружает шаблоны активностей для разных возрастов и тем"""
        return {
            "warm_up": {
                "1-3": [
                    LessonActivity(
                        "Музыкальная разминка",
                        ActivityType.SONG,
                        3,
                        "Простая песенка с движениями для самых маленьких",
                        ["аудиозапись", "игрушки"],
                        [
                            "Включить веселую музыку",
                            "Показать простые движения",
                            "Повторять движения вместе с детьми",
                            "Использовать игрушки для привлечения внимания"
                        ],
                        learning_objectives=["Привлечь внимание", "Создать позитивное настроение", "Активировать моторику"],
                        difficulty_level="easy",
                        preparation_time=2,
                        cleanup_time=1,
                        alternative_activities=["Игра с мячом", "Простая зарядка"],
                        assessment_criteria=["Участие в движениях", "Эмоциональная реакция", "Повторение движений"],
                        safety_notes=["Убедитесь в безопасности пространства", "Следите за детьми во время движений"],
                        technology_requirements=["Аудиосистема", "Музыкальная запись"]
                    )
                ],
                "3-6": [
                    LessonActivity(
                        "Приветственная песня",
                        ActivityType.SONG,
                        5,
                        "Веселая песня с движениями",
                        ["колонка", "карточки с эмоциями"],
                        [
                            "Включить музыку",
                            "Показать движения",
                            "Петь вместе с детьми",
                            "Использовать карточки для показа эмоций"
                        ],
                    ),
                    LessonActivity(
                        "Игра с мячом",
                        ActivityType.GAME,
                        5,
                        "Передача мяча с называнием слов",
                        ["мяч", "карточки"],
                        [
                            "Встать в круг",
                            "Передавать мяч по кругу",
                            "Каждый называет слово на английском",
                            "Поощрять правильное произношение"
                        ],
                    )
                ],
                "6-9": [
                    LessonActivity(
                        "Вопрос-ответ",
                        ActivityType.DIALOGUE,
                        5,
                        "Быстрые вопросы о настроении и погоде",
                        ["карточки с вопросами"],
                        [
                            "Задать вопрос 'How are you?'",
                            "Дети отвечают",
                            "Спросить о погоде",
                            "Использовать карточки для визуальной поддержки"
                        ],
                    ),
                    LessonActivity(
                        "Алфавитная разминка",
                        ActivityType.GAME,
                        5,
                        "Повторение букв алфавита с движениями",
                        ["карточки с буквами"],
                        [
                            "Показать букву",
                            "Дети называют букву и слово на эту букву",
                            "Выполняют движение, связанное со словом",
                            "Повторяют хором"
                        ],
                    )
                ],
                "9-12": [
                    LessonActivity(
                        "Быстрая викторина",
                        ActivityType.QUIZ,
                        5,
                        "Вопросы на общие знания на английском",
                        ["карточки с вопросами", "табло для подсчета"],
                        [
                            "Задать вопрос на английском",
                            "Дети поднимают руки для ответа",
                            "Объяснить правильный ответ",
                            "Вести счет правильных ответов"
                        ],
                    )
                ],
                "12-15": [
                    LessonActivity(
                        "Обсуждение новостей",
                        ActivityType.DIALOGUE,
                        5,
                        "Краткое обсуждение актуальных тем",
                        ["газеты", "журналы", "интернет"],
                        [
                            "Предложить тему для обсуждения",
                            "Выслушать мнения учеников",
                            "Задать уточняющие вопросы",
                            "Поощрять использование новой лексики"
                        ],
                    )
                ]
            },
            "vocabulary": {
                "животные": [
                    LessonActivity(
                        "Угадай животное",
                        ActivityType.GAME,
                        10,
                        "Дети угадывают животных по звукам и описанию",
                        ["карточки животных", "аудиозаписи звуков"],
                        [
                            "Показать карточку",
                            "Издать звук животного",
                            "Дети угадывают название",
                            "Повторить слово хором",
                            "Показать транскрипцию"
                        ],
                    ),
                    LessonActivity(
                        "Зоопарк в классе",
                        ActivityType.CRAFT,
                        15,
                        "Создание зоопарка из подручных материалов",
                        ["цветная бумага", "клей", "ножницы", "карандаши"],
                        [
                            "Раздать материалы",
                            "Каждый выбирает животное",
                            "Создать поделку",
                            "Рассказать о своем животном на английском"
                        ],
                    )
                ],
                "цвета": [
                    LessonActivity(
                        "Охота за цветами",
                        ActivityType.GAME,
                        10,
                        "Найти предметы определенного цвета в комнате",
                        ["цветные карточки", "мелкие призы"],
                        [
                            "Назвать цвет на английском",
                            "Дети находят предметы этого цвета",
                            "Назвать предметы на английском",
                            "Повторить цвета хором"
                        ],
                    ),
                    LessonActivity(
                        "Раскрашивание по номерам",
                        ActivityType.CRAFT,
                        15,
                        "Раскрашивание картинки с использованием английских названий цветов",
                        ["раскраски", "цветные карандаши", "инструкции на английском"],
                        [
                            "Раздать раскраски",
                            "Прочитать инструкции на английском",
                            "Дети раскрашивают по инструкции",
                            "Проверить правильность выполнения"
                        ],
                    )
                ],
                "еда": [
                    LessonActivity(
                        "Ресторан в классе",
                        ActivityType.DIALOGUE,
                        15,
                        "Ролевая игра в ресторане",
                        ["игрушечная еда", "меню", "аптечка"],
                        [
                            "Раздать роли (официант, клиент)",
                            "Изучить меню на английском",
                            "Разыграть диалог заказа",
                            "Использовать вежливые фразы"
                        ],
                    )
                ],
                "семья": [
                    LessonActivity(
                        "Семейное дерево",
                        ActivityType.CRAFT,
                        15,
                        "Создание семейного дерева с английскими названиями",
                        ["бумага", "фотографии", "клей", "карандаши"],
                        [
                            "Принести фотографии семьи",
                            "Создать семейное дерево",
                            "Подписать родственников на английском",
                            "Рассказать о семье"
                        ],
                    )
                ]
            },
            "practice": {
                "1-3": [
                    LessonActivity(
                        "Повторение с игрушками",
                        ActivityType.GAME,
                        8,
                        "Изучение слов через игру с игрушками",
                        ["игрушки", "карточки"],
                        [
                            "Показать игрушку",
                            "Назвать слово на английском",
                            "Дети повторяют",
                            "Играть с игрушкой"
                        ],
                    )
                ],
                "3-6": [
                    LessonActivity(
                        "Музыкальные стулья",
                        ActivityType.GAME,
                        10,
                        "Классическая игра с английскими словами",
                        ["стулья", "музыка", "карточки"],
                        [
                            "Расставить стулья по кругу",
                            "Включить музыку",
                            "Дети ходят вокруг стульев",
                            "Когда музыка останавливается, назвать слово на английском"
                        ],
                    )
                ],
                "6-9": [
                    LessonActivity(
                        "Словарный бой",
                        ActivityType.GAME,
                        12,
                        "Соревнование на знание слов",
                        ["карточки", "табло", "призы"],
                        [
                            "Разделить на команды",
                            "Показать карточку",
                            "Команды по очереди называют слово",
                            "Вести счет очков"
                        ],
                    )
                ],
                "9-12": [
                    LessonActivity(
                        "Дебаты",
                        ActivityType.DIALOGUE,
                        15,
                        "Обсуждение темы на английском языке",
                        ["карточки с темами", "таймер"],
                        [
                            "Выбрать тему для обсуждения",
                            "Разделить на группы",
                            "Подготовить аргументы",
                            "Провести дебаты"
                        ],
                    )
                ],
                "12-15": [
                    LessonActivity(
                        "Проектная работа",
                        ActivityType.CRAFT,
                        20,
                        "Создание проекта по теме урока",
                        ["компьютеры", "принтер", "материалы для презентации"],
                        [
                            "Выбрать тему проекта",
                            "Исследовать информацию",
                            "Создать презентацию",
                            "Представить проект классу"
                        ],
                    )
                ]
            }
        }

    def start(self):
        print("🚀 КОНСТРУКТОР УРОКОВ АНГЛИЙСКОГО ДЛЯ ДЕТЕЙ")
        print("=" * 50)

        while True:
            lesson = self._create_lesson_interactive()
            if lesson:
                print("\n" + "=" * 50)
                print(lesson.get_lesson_plan())
                print("=" * 50)

                save = input("\n💾 Сохранить этот урок? (д/н): ").lower()
                if save == "д":
                    self._save_lesson(lesson)

                another = input("\n🔄 Создать еще один урок? (д/н): ").lower()
                if another != "д":
                    print("👋 До свидания!")
                    break

    def _create_lesson_interactive(self):
        print("\n" + "=" * 50)
        print("Создание нового урока")
        print("=" * 50)

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
        print("  1. beginner (базовый)")

        try:
            level_choice = int(input("Введите номер уровня: ")) - 1
            en_level = "beginner"  # Фиксированный уровень
        except (ValueError, IndexError):
            print("❌ Неверный выбор уровня!")
            return None

        # Длительность урока
        try:
            duration = int(
                input("\n⏱️  Введите длительность урока (в минутах, 30-60): ")
            )
            if duration < 30 or duration > 60:
                print("⚠️  Длительность установлена 45 минут")
                duration = 45
        except ValueError:
            print("⚠️  Длительность установлена 45 минут")
            duration = 45

        # Создание урока
        return self._generate_lesson(theme, age_group, duration)

    def _generate_lesson(
        self, theme: str, age_group: AgeGroup, duration: int
    ) -> Lesson:
        # Получаем шаблон урока
        template = self._get_lesson_template(age_group, en_level)
        
        # Генерация названия на основе шаблона
        title = template["title_template"].format(theme=theme.title())

        # Цели урока
        objectives = self._generate_objectives(theme, age_group)

        # Словарный запас с детальной информацией
        vocabulary = self._get_vocabulary_with_details(theme, age_group)

        # Активности с использованием шаблона
        activities = self._generate_activities_with_template(
            theme, age_group, en_level, duration, template
        )

        # Генерируем дополнительные поля
        lesson_phases = self._generate_lesson_phases(theme, age_group, en_level, duration)
        materials_summary = self._generate_materials_summary(activities, theme, age_group)
        assessment_methods = self._generate_assessment_methods(age_group, en_level)
        homework_suggestions = self._generate_homework_suggestions(theme, age_group, en_level)
        extension_activities = self._generate_extension_activities(theme, age_group, en_level)
        cultural_notes = self._generate_cultural_notes(theme, age_group, en_level)
        common_mistakes = self._generate_common_mistakes(theme, age_group, en_level)
        teacher_notes = self._generate_teacher_notes(theme, age_group, en_level, template)
        student_handouts = self._generate_student_handouts(theme, age_group, en_level)
        technology_tools = self._generate_technology_tools(age_group, en_level)
        room_setup = self._generate_room_setup(age_group, en_level)
        group_size = self._generate_group_size(age_group, en_level)
        prerequisites = self._generate_prerequisites(theme, age_group, en_level)

        return Lesson(
            title,
            theme,
            age_group,
            en_level,
            duration,
            objectives,
            activities,
            vocabulary,
            lesson_phases,
            materials_summary,
            assessment_methods,
            homework_suggestions,
            extension_activities,
            cultural_notes,
            common_mistakes,
            teacher_notes,
            student_handouts,
            technology_tools,
            room_setup,
            group_size,
            prerequisites,
        )

    def _generate_objectives(
        self, theme: str, age_group: AgeGroup
    ) -> List[str]:
<<<<<<< HEAD
        """Генерирует образовательные цели на основе возраста и уровня"""
        age_key = age_group.value
        level_key = level.value
        
        # Получаем цели из загруженных шаблонов
        if age_key in self.learning_objectives and level_key in self.learning_objectives[age_key]:
            return self.learning_objectives[age_key][level_key]
        
        # Fallback цели по умолчанию
        fallback_objectives = {
            "beginner": [
                "Познакомиться с базовой лексикой по теме",
                "Научиться произносить новые слова",
                "Развить интерес к английскому через игры",
            ],
            "elementary": [
                "Расширить словарный запас по теме",
                "Научиться строить простые предложения",
                "Потренировать аудирование и говорение",
            ],
            "intermediate": [
                "Закрепить лексику по теме",
                "Практиковать диалогическую речь",
                "Развить коммуникативные навыки",
            ],
            "upper-intermediate": [
                "Использовать сложную лексику по теме",
                "Вести дискуссии на английском языке",
                "Развить навыки критического мышления",
            ],
        }
        
        return fallback_objectives.get(level_key, ["Развить языковые навыки"])

    def _generate_lesson_phases(self, theme: str, age_group: AgeGroup, en_level: EnglishLevel, duration: int) -> List[dict]:
        """Генерирует детальные фазы урока"""
        age_key = age_group.value
        level_key = en_level.value
        
        phases = []
        
        # Разминка
        warm_up_duration = 5 if age_key in ["1-3", "3-6"] else 7 if age_key in ["6-9"] else 10
        phases.append({
            "name": "Разминка и мотивация",
            "duration": warm_up_duration,
            "description": "Активизация внимания и создание позитивной атмосферы",
            "objectives": ["Привлечь внимание учащихся", "Создать мотивацию к изучению", "Активировать предыдущие знания"]
        })
        
        # Введение лексики
        vocab_duration = int(duration * 0.3) if age_key in ["1-3", "3-6"] else int(duration * 0.25)
        phases.append({
            "name": "Введение новой лексики",
            "duration": vocab_duration,
            "description": f"Изучение новых слов по теме '{theme}'",
            "objectives": ["Познакомить с новой лексикой", "Отработать произношение", "Обеспечить понимание значений"]
        })
        
        # Практика
        practice_duration = int(duration * 0.4) if age_key in ["1-3", "3-6"] else int(duration * 0.45)
        phases.append({
            "name": "Практическое применение",
            "duration": practice_duration,
            "description": "Закрепление изученного материала через активную деятельность",
            "objectives": ["Закрепить новую лексику", "Развить навыки говорения", "Повысить уверенность в использовании языка"]
        })
        
        # Творческая активность
        creative_duration = int(duration * 0.15) if age_key in ["1-3", "3-6"] else int(duration * 0.2)
        phases.append({
            "name": "Творческое закрепление",
            "duration": creative_duration,
            "description": "Применение знаний в творческих заданиях",
            "objectives": ["Проявить креативность", "Использовать изученную лексику в контексте", "Развить воображение"]
        })
        
        # Завершение
        wrap_up_duration = duration - sum(phase["duration"] for phase in phases)
        phases.append({
            "name": "Подведение итогов и рефлексия",
            "duration": wrap_up_duration,
            "description": "Обобщение изученного материала и планирование дальнейшего обучения",
            "objectives": ["Закрепить ключевые моменты", "Оценить достижения", "Мотивировать к дальнейшему изучению"]
        })
        
        return phases

    def _generate_materials_summary(self, activities: List[LessonActivity], theme: str, age_group: AgeGroup) -> List[str]:
        """Генерирует общий список материалов для урока"""
        materials = set()
        
        # Собираем материалы из всех активностей
        for activity in activities:
            materials.update(activity.materials)
        
        # Добавляем базовые материалы в зависимости от возраста
        age_key = age_group.value
        
        if age_key in ["1-3", "3-6"]:
            materials.update([
                "Цветные карандаши и фломастеры",
                "Бумага для рисования",
                "Клей и ножницы (детские)",
                "Игрушки по теме урока",
                "Аудиосистема для музыки",
                "Карточки с картинками"
            ])
        elif age_key in ["6-9"]:
            materials.update([
                "Тетради и ручки",
                "Цветные карандаши",
                "Карточки со словами",
                "Игровые материалы",
                "Аудиосистема",
                "Проектор или интерактивная доска"
            ])
        else:
            materials.update([
                "Тетради и ручки",
                "Учебные материалы",
                "Компьютеры или планшеты",
                "Интерактивная доска",
                "Аудиосистема",
                "Раздаточные материалы"
            ])
        
        # Добавляем материалы в зависимости от темы
        theme_materials = {
            "животные": ["Фигурки животных", "Карточки с животными", "Звуки животных"],
            "цвета": ["Цветные карточки", "Краски", "Цветная бумага"],
            "еда": ["Игрушечная еда", "Меню", "Карточки с продуктами"],
            "семья": ["Фотографии семьи", "Семейное дерево", "Карточки с родственниками"],
            "музыка": ["Музыкальные инструменты", "Аудиозаписи", "Ноты"]
        }
        
        if theme in theme_materials:
            materials.update(theme_materials[theme])
        
        return sorted(list(materials))

    def _generate_assessment_methods(self, age_group: AgeGroup, en_level: EnglishLevel) -> List[str]:
        """Генерирует методы оценки для урока"""
        age_key = age_group.value
        level_key = en_level.value
        
        methods = []
        
        if age_key in ["1-3", "3-6"]:
            methods = [
                "Наблюдение за активностью и участием",
                "Проверка понимания через жесты и мимику",
                "Оценка способности повторять слова",
                "Наблюдение за интересом к активности"
            ]
        elif age_key in ["6-9"]:
            methods = [
                "Устные ответы на вопросы",
                "Выполнение игровых заданий",
                "Проверка произношения слов",
                "Наблюдение за участием в групповых активностях",
                "Простые тесты на понимание"
            ]
        elif age_key in ["9-12"]:
            methods = [
                "Устные презентации",
                "Письменные задания",
                "Групповые проекты",
                "Тесты на понимание",
                "Самооценка и взаимооценка",
                "Портфолио работ"
            ]
        else:  # 12-15
            methods = [
                "Презентации и проекты",
                "Эссе и сочинения",
                "Дебаты и дискуссии",
                "Тесты и экзамены",
                "Портфолио достижений",
                "Самооценка и рефлексия"
            ]
        
        return methods

    def _generate_homework_suggestions(self, theme: str, age_group: AgeGroup, en_level: EnglishLevel) -> List[str]:
        """Генерирует предложения по домашнему заданию"""
        age_key = age_group.value
        level_key = en_level.value
        
        suggestions = []
        
        if age_key in ["1-3", "3-6"]:
            suggestions = [
                f"Показать родителям карточки с {theme}",
                "Спеть изученную песенку дома",
                "Нарисовать картинку по теме урока",
                "Показать жесты, изученные на уроке"
            ]
        elif age_key in ["6-9"]:
            suggestions = [
                f"Написать 5 слов по теме '{theme}'",
                "Нарисовать картинку и подписать на английском",
                "Показать родителям, что изучили",
                "Повторить слова перед зеркалом"
            ]
        elif age_key in ["9-12"]:
            suggestions = [
                f"Написать короткий рассказ о {theme}",
                "Создать презентацию по теме",
                "Найти дополнительную информацию в интернете",
                "Попрактиковаться с онлайн-упражнениями"
            ]
        else:  # 12-15
            suggestions = [
                f"Написать эссе о {theme}",
                "Создать видео-презентацию",
                "Исследовать культурные аспекты темы",
                "Подготовить материал для следующего урока"
            ]
        
        return suggestions

    def _generate_extension_activities(self, theme: str, age_group: AgeGroup, en_level: EnglishLevel) -> List[str]:
        """Генерирует дополнительные активности для продвинутых учеников"""
        age_key = age_group.value
        
        activities = []
        
        if age_key in ["1-3", "3-6"]:
            activities = [
                "Дополнительные игры с изученными словами",
                "Создание собственных песенок",
                "Дополнительное рисование и раскрашивание"
            ]
        elif age_key in ["6-9"]:
            activities = [
                "Создание собственных карточек",
                "Написание коротких историй",
                "Организация мини-спектакля"
            ]
        elif age_key in ["9-12"]:
            activities = [
                "Создание блога по теме",
                "Организация дебатов",
                "Создание викторины для одноклассников"
            ]
        else:  # 12-15
            activities = [
                "Создание подкаста по теме",
                "Организация конференции",
                "Создание образовательного контента"
            ]
        
        return activities

    def _generate_cultural_notes(self, theme: str, age_group: AgeGroup, en_level: EnglishLevel) -> List[str]:
        """Генерирует культурные заметки по теме"""
        cultural_notes = {
            "животные": [
                "В англоязычных странах кошки и собаки - самые популярные домашние животные",
                "В Великобритании красные лисы считаются символом дикой природы",
                "В Австралии кенгуру - национальный символ"
            ],
            "цвета": [
                "В западной культуре белый цвет символизирует чистоту и невинность",
                "Красный цвет в Китае символизирует удачу и счастье",
                "В США красный, белый и синий - цвета национального флага"
            ],
            "еда": [
                "Fish and chips - традиционное британское блюдо",
                "В США популярны гамбургеры и хот-доги",
                "Послеобеденный чай - британская традиция"
            ],
            "семья": [
                "В англоязычных странах принято называть родителей по имени",
                "Семейные ужины - важная традиция в США и Великобритании",
                "День матери и День отца отмечаются в разные дни"
            ]
        }
        
        return cultural_notes.get(theme, [
            "Изучение языка помогает понять культуру других стран",
            "Важно уважать культурные различия при изучении языка"
        ])

    def _generate_common_mistakes(self, theme: str, age_group: AgeGroup, en_level: EnglishLevel) -> List[str]:
        """Генерирует список частых ошибок и способов их избежать"""
        age_key = age_group.value
        level_key = en_level.value
        
        mistakes = []
        
        if level_key == "beginner":
            mistakes = [
                "Смешивание звуков [θ] и [s] - практикуйте произношение 'th'",
                "Неправильный порядок слов в предложении - изучайте базовую структуру",
                "Забывание артиклей 'a', 'an', 'the' - запоминайте правила использования"
            ]
        elif level_key == "elementary":
            mistakes = [
                "Неправильное использование времен - изучайте Present Simple и Present Continuous",
                "Смешивание 'much' и 'many' - запоминайте: much с неисчисляемыми, many с исчисляемыми",
                "Неправильное произношение окончаний -ed в прошедшем времени"
            ]
        elif level_key == "intermediate":
            mistakes = [
                "Неправильное использование Present Perfect - изучайте контекст использования",
                "Смешивание 'few' и 'little' - few с исчисляемыми, little с неисчисляемыми",
                "Неправильный порядок прилагательных - запоминайте: мнение, размер, возраст, цвет"
            ]
        else:  # upper-intermediate
            mistakes = [
                "Неправильное использование условных предложений - изучайте типы условий",
                "Смешивание 'affect' и 'effect' - affect (глагол), effect (существительное)",
                "Неправильное использование предлогов в фразовых глаголах"
            ]
        
        return mistakes

    def _generate_teacher_notes(self, theme: str, age_group: AgeGroup, en_level: EnglishLevel, template: dict) -> List[str]:
        """Генерирует заметки для учителя"""
        age_key = age_group.value
        level_key = en_level.value
        
        notes = []
        
        # Базовые заметки
        notes.extend([
            "Подготовьте все материалы заранее",
            "Проверьте техническое оборудование",
            "Создайте позитивную атмосферу в классе"
        ])
        
        # Возрастные особенности
        if age_key in ["1-3", "3-6"]:
            notes.extend([
                "Используйте много визуальных материалов",
                "Делайте частые перерывы для движения",
                "Повторяйте слова и фразы многократно",
                "Поощряйте любое проявление активности"
            ])
        elif age_key in ["6-9"]:
            notes.extend([
                "Включайте элементы игры в каждую активность",
                "Используйте соревновательные элементы",
                "Поощряйте самостоятельность",
                "Связывайте материал с личным опытом детей"
            ])
        elif age_key in ["9-12"]:
            notes.extend([
                "Поощряйте критическое мышление",
                "Используйте групповые работы",
                "Связывайте материал с реальной жизнью",
                "Включайте элементы исследования"
            ])
        else:  # 12-15
            notes.extend([
                "Поощряйте самостоятельное изучение",
                "Используйте современные технологии",
                "Развивайте навыки презентации",
                "Связывайте с будущими целями учащихся"
            ])
        
        # Специальные инструкции из шаблона
        if "special_instructions" in template:
            notes.extend(template["special_instructions"])
        
        return notes

    def _generate_student_handouts(self, theme: str, age_group: AgeGroup, en_level: EnglishLevel) -> List[str]:
        """Генерирует список раздаточных материалов"""
        age_key = age_group.value
        
        handouts = []
        
        if age_key in ["1-3", "3-6"]:
            handouts = [
                "Раскраски по теме",
                "Карточки с картинками",
                "Простые задания на соединение"
            ]
        elif age_key in ["6-9"]:
            handouts = [
                "Рабочие листы с заданиями",
                "Карточки со словами",
                "Игровые поля",
                "Простые тесты"
            ]
        elif age_key in ["9-12"]:
            handouts = [
                "Информационные листы",
                "Задания для групповой работы",
                "Шаблоны для проектов",
                "Словари и справочники"
            ]
        else:  # 12-15
            handouts = [
                "Подробные инструкции",
                "Материалы для исследований",
                "Шаблоны для презентаций",
                "Справочные материалы"
            ]
        
        return handouts

    def _generate_technology_tools(self, age_group: AgeGroup, en_level: EnglishLevel) -> List[str]:
        """Генерирует список технологических инструментов"""
        age_key = age_group.value
        
        tools = []
        
        if age_key in ["1-3", "3-6"]:
            tools = [
                "Аудиосистема для музыки",
                "Проектор для показа картинок",
                "Простые образовательные приложения"
            ]
        elif age_key in ["6-9"]:
            tools = [
                "Интерактивная доска",
                "Планшеты с образовательными приложениями",
                "Аудиосистема",
                "Проектор"
            ]
        elif age_key in ["9-12"]:
            tools = [
                "Компьютеры или ноутбуки",
                "Интерактивная доска",
                "Онлайн-словари и переводчики",
                "Образовательные веб-сайты"
            ]
        else:  # 12-15
            tools = [
                "Компьютеры с доступом в интернет",
                "Программы для создания презентаций",
                "Онлайн-платформы для обучения",
                "Мобильные приложения для изучения языка"
            ]
        
        return tools

    def _generate_room_setup(self, age_group: AgeGroup, en_level: EnglishLevel) -> str:
        """Генерирует описание организации пространства"""
        age_key = age_group.value
        
        if age_key in ["1-3", "3-6"]:
            return "Круг из стульев или ковер в центре, пространство для движения, столы для творческих активностей"
        elif age_key in ["6-9"]:
            return "Столы, расставленные для групповой работы, доска в центре, пространство для игр"
        elif age_key in ["9-12"]:
            return "Столы для групповой работы, интерактивная доска, компьютерная зона"
        else:  # 12-15
            return "Столы для групповой работы, мультимедийное оборудование, зона для презентаций"

    def _generate_group_size(self, age_group: AgeGroup, en_level: EnglishLevel) -> str:
        """Генерирует рекомендуемый размер группы"""
        age_key = age_group.value
        
        if age_key in ["1-3", "3-6"]:
            return "4-8 человек"
        elif age_key in ["6-9"]:
            return "6-12 человек"
        elif age_key in ["9-12"]:
            return "8-15 человек"
        else:  # 12-15
            return "10-20 человек"

    def _generate_prerequisites(self, theme: str, age_group: AgeGroup, en_level: EnglishLevel) -> List[str]:
        """Генерирует список предварительных знаний"""
        age_key = age_group.value
        level_key = en_level.value
        
        prerequisites = []
        
        if level_key == "beginner":
            prerequisites = [
                "Базовое понимание английского алфавита",
                "Знание простых приветствий",
                "Способность повторять звуки и слова"
            ]
        elif level_key == "elementary":
            prerequisites = [
                "Знание базовой лексики",
                "Понимание простых инструкций",
                "Способность строить простые предложения"
            ]
        elif level_key == "intermediate":
            prerequisites = [
                "Знание основных времен английского языка",
                "Способность вести простые диалоги",
                "Понимание текстов средней сложности"
            ]
        else:  # upper-intermediate
            prerequisites = [
                "Свободное владение основными грамматическими структурами",
                "Способность выражать сложные идеи",
                "Понимание аутентичных текстов"
            ]
        
        return prerequisites

    def _load_lesson_templates(self):
        """Загружает шаблоны уроков для разных комбинаций возраста и уровня"""
        return {
            "1-3_beginner": {
                "title_template": "Первые шаги в английском: {theme}",
                "structure": {
                    "warm_up_ratio": 0.3,
                    "vocabulary_ratio": 0.5,
                    "practice_ratio": 0.2
                },
                "special_instructions": [
                    "Использовать много визуальных материалов",
                    "Повторять слова по 3-5 раз",
                    "Делать частые перерывы",
                    "Использовать игрушки и предметы"
                ]
            },
            "3-6_beginner": {
                "title_template": "Играем и изучаем: {theme}",
                "structure": {
                    "warm_up_ratio": 0.2,
                    "vocabulary_ratio": 0.4,
                    "practice_ratio": 0.3,
                    "creative_ratio": 0.1
                },
                "special_instructions": [
                    "Включать движения и танцы",
                    "Использовать песни и рифмы",
                    "Поощрять активное участие",
                    "Создавать игровую атмосферу"
                ]
            },
            "6-9_elementary": {
                "title_template": "Английский с удовольствием: {theme}",
                "structure": {
                    "warm_up_ratio": 0.15,
                    "vocabulary_ratio": 0.35,
                    "practice_ratio": 0.35,
                    "creative_ratio": 0.15
                },
                "special_instructions": [
                    "Включать элементы соревнования",
                    "Использовать карточки и игры",
                    "Поощрять самостоятельность",
                    "Связывать с реальной жизнью"
                ]
            },
            "9-12_intermediate": {
                "title_template": "Углубляем знания: {theme}",
                "structure": {
                    "warm_up_ratio": 0.1,
                    "vocabulary_ratio": 0.25,
                    "practice_ratio": 0.45,
                    "creative_ratio": 0.2
                },
                "special_instructions": [
                    "Включать дискуссии и дебаты",
                    "Использовать аутентичные материалы",
                    "Развивать критическое мышление",
                    "Связывать с культурой англоязычных стран"
                ]
            },
            "12-15_upper-intermediate": {
                "title_template": "Мастер-класс по английскому: {theme}",
                "structure": {
                    "warm_up_ratio": 0.1,
                    "vocabulary_ratio": 0.2,
                    "practice_ratio": 0.5,
                    "creative_ratio": 0.2
                },
                "special_instructions": [
                    "Включать проекты и исследования",
                    "Использовать современные технологии",
                    "Развивать навыки презентации",
                    "Подготавливать к реальному использованию языка"
                ]
            }
        }

    def _get_lesson_template(self, age_group: AgeGroup, level: EnglishLevel):
        """Получает шаблон урока для конкретной комбинации возраста и уровня"""
        age_key = age_group.value
        level_key = level.value
        
        # Ищем точное совпадение
        template_key = f"{age_key}_{level_key}"
        if template_key in self.lesson_templates:
            return self.lesson_templates[template_key]
        
        # Ищем ближайший подходящий шаблон
        for template_key, template in self.lesson_templates.items():
            template_age, template_level = template_key.split("_")
            
            # Проверяем совпадение возраста
            age_match = False
            if template_age == age_key:
                age_match = True
            elif template_age in ["1-3", "3-6"] and age_key in ["1-3", "3-6"]:
                age_match = True
            elif template_age in ["6-9", "9-12"] and age_key in ["6-9", "9-12"]:
                age_match = True
            elif template_age == "12-15" and age_key == "12-15":
                age_match = True
            
            # Проверяем совпадение уровня
            level_match = False
            if template_level == level_key:
                level_match = True
            elif template_level == "beginner" and level_key in ["beginner", "elementary"]:
                level_match = True
            elif template_level == "elementary" and level_key in ["elementary", "intermediate"]:
                level_match = True
            elif template_level == "intermediate" and level_key in ["intermediate", "upper-intermediate"]:
                level_match = True
            
            if age_match and level_match:
                return template
        
        # Возвращаем базовый шаблон
        return {
            "title_template": "Урок английского: {theme}",
            "structure": {
                "warm_up_ratio": 0.15,
                "vocabulary_ratio": 0.35,
                "practice_ratio": 0.35,
                "creative_ratio": 0.15
            },
            "special_instructions": [
                "Адаптировать под конкретную группу",
                "Использовать разнообразные методы",
                "Поддерживать интерес учащихся"
            ]
        }
=======
        # Упрощенные цели без уровней
        base_objectives = [
            "Познакомиться с базовой лексикой по теме",
            "Научиться произносить новые слова",
            "Развить интерес к английскому через игры",
            "Практиковать говорение в игровой форме"
        ]
        
        return base_objectives
>>>>>>> origin/NIKITA

    def _generate_vocabulary(self, theme: str, age_group: AgeGroup) -> List[str]:
        """Генерирует словарный запас с учетом возраста и темы"""
        # Определяем лимит слов по возрасту
        word_limit = {"1-3": 3, "3-6": 4, "6-9": 6, "9-12": 8, "12-15": 10}
        limit = word_limit.get(age_group.value, 5)

        # Пытаемся получить слова из базы данных
        if self.db_get_words:
            try:
                words = self.db_get_words(theme, limit)
                if words:
                    return words
            except Exception as e:
                print(f"⚠️  Не удалось получить слова из БД: {e}")

        # Если не получилось из БД, используем расширенный fallback словарь
        vocabulary_bank = {
            "животные": ["cat", "dog", "bird", "fish", "rabbit", "lion", "elephant", "tiger", "bear", "horse"],
            "цвета": ["red", "blue", "green", "yellow", "orange", "purple", "pink", "black", "white", "brown"],
            "еда": ["apple", "banana", "milk", "bread", "juice", "water", "cake", "cookie", "cheese", "egg"],
            "семья": ["mother", "father", "sister", "brother", "grandma", "grandpa", "baby", "uncle", "aunt", "cousin"],
            "одежда": ["dress", "shirt", "pants", "shoes", "hat", "socks", "jacket", "coat", "skirt", "boots"],
            "дом": ["house", "room", "bed", "table", "chair", "window", "door", "kitchen", "bathroom", "bedroom"],
            "школа": ["book", "pen", "pencil", "teacher", "student", "classroom", "desk", "backpack", "paper", "notebook"],
            "хобби": ["read", "draw", "sing", "dance", "play", "swim", "run", "jump", "walk", "ride"],
            "погода": ["sun", "rain", "snow", "cloud", "wind", "hot", "cold", "warm", "cool", "sky"],
            "игрушки": ["toy", "ball", "doll", "car", "bike", "puzzle", "blocks", "teddy", "robot", "game"],
            "природа": ["tree", "flower", "grass", "moon", "star", "mountain", "river", "ocean", "forest", "garden"],
            "транспорт": ["car", "bus", "train", "plane", "bike", "boat", "truck", "motorcycle", "taxi", "subway"],
            "спорт": ["football", "basketball", "tennis", "swimming", "running", "cycling", "dancing", "gymnastics", "boxing", "yoga"],
            "музыка": ["piano", "guitar", "drum", "violin", "song", "music", "dance", "sing", "concert", "band"],
            "искусство": ["paint", "draw", "color", "picture", "art", "museum", "gallery", "artist", "brush", "canvas"]
        }

        words = vocabulary_bank.get(theme, [])
<<<<<<< HEAD
        return words[:limit]

    def _get_vocabulary_with_details(self, theme: str, age_group: AgeGroup) -> List[dict]:
        """Получает словарный запас с детальной информацией (слово, транскрипция, перевод)"""
        # Определяем лимит слов по возрасту
        word_limit = {"1-3": 3, "3-6": 4, "6-9": 6, "9-12": 8, "12-15": 10}
        limit = word_limit.get(age_group.value, 5)

        # Пытаемся получить детальную информацию из базы данных
        try:
            from db_service import db_get_words_with_details
            words_details = db_get_words_with_details(theme, limit)
            if words_details:
                return words_details
        except Exception as e:
            print(f"⚠️  Не удалось получить детальную информацию из БД: {e}")

        # Fallback - создаем детальную информацию из простого списка слов
        simple_words = self._generate_vocabulary(theme, age_group)
        words_details = []
        
        # Базовые транскрипции и переводы (упрощенные)
        basic_translations = {
            "cat": ("kæt", "кот"),
            "dog": ("dɔːɡ", "собака"),
            "bird": ("bɜːrd", "птица"),
            "fish": ("fɪʃ", "рыба"),
            "rabbit": ("ˈræbɪt", "кролик"),
            "lion": ("ˈlaɪən", "лев"),
            "elephant": ("ˈelɪfənt", "слон"),
            "red": ("red", "красный"),
            "blue": ("bluː", "синий"),
            "green": ("ɡriːn", "зеленый"),
            "yellow": ("ˈjeloʊ", "желтый"),
            "apple": ("ˈæpl", "яблоко"),
            "banana": ("bəˈnænə", "банан"),
            "milk": ("mɪlk", "молоко"),
            "bread": ("bred", "хлеб"),
            "mother": ("ˈmʌðər", "мама"),
            "father": ("ˈfɑːðər", "папа"),
            "sister": ("ˈsɪstər", "сестра"),
            "brother": ("ˈbrʌðər", "брат"),
            "house": ("haʊs", "дом"),
            "book": ("bʊk", "книга"),
            "pen": ("pen", "ручка"),
            "pencil": ("ˈpensl", "карандаш"),
            "teacher": ("ˈtiːtʃər", "учитель"),
            "student": ("ˈstuːdnt", "ученик"),
            "read": ("riːd", "читать"),
            "draw": ("drɔː", "рисовать"),
            "sing": ("sɪŋ", "петь"),
            "dance": ("dæns", "танцевать"),
            "play": ("pleɪ", "играть"),
            "sun": ("sʌn", "солнце"),
            "rain": ("reɪn", "дождь"),
            "snow": ("snoʊ", "снег"),
            "toy": ("tɔɪ", "игрушка"),
            "ball": ("bɔːl", "мяч"),
            "tree": ("triː", "дерево"),
            "flower": ("ˈflaʊər", "цветок"),
            "car": ("kɑːr", "машина"),
            "bus": ("bʌs", "автобус"),
            "train": ("treɪn", "поезд"),
            "plane": ("pleɪn", "самолет"),
            "bike": ("baɪk", "велосипед"),
            "football": ("ˈfʊtbɔːl", "футбол"),
            "basketball": ("ˈbæskɪtbɔːl", "баскетбол"),
            "tennis": ("ˈtenɪs", "теннис"),
            "swimming": ("ˈswɪmɪŋ", "плавание"),
            "running": ("ˈrʌnɪŋ", "бег"),
            "piano": ("piˈænoʊ", "пианино"),
            "guitar": ("ɡɪˈtɑːr", "гитара"),
            "drum": ("drʌm", "барабан"),
            "violin": ("ˌvaɪəˈlɪn", "скрипка"),
            "paint": ("peɪnt", "краска"),
            "draw": ("drɔː", "рисовать"),
            "color": ("ˈkʌlər", "цвет"),
            "picture": ("ˈpɪktʃər", "картина"),
            "art": ("ɑːrt", "искусство")
        }
        
        for word in simple_words:
            if word in basic_translations:
                transcription, translation = basic_translations[word]
                words_details.append({
                    "word": word,
                    "transcription": transcription,
                    "translation": translation
                })
            else:
                # Если нет детальной информации, используем только слово
                words_details.append({
                    "word": word,
                    "transcription": "[произношение]",
                    "translation": "[перевод]"
                })
        
        return words_details
=======
        # Ограничиваем количество слов по возрасту
        word_limit = {"1-3": 3, "4-7": 5, "8-15": 8}
        return words[: word_limit.get(age_group.value, 5)]
>>>>>>> origin/NIKITA

    def _generate_activities(
        self, theme: str, age_group: AgeGroup, duration: int
    ) -> List[LessonActivity]:
        """Генерирует адаптивные активности для урока"""
        activities = []
        age_key = age_group.value

        # Разминка (5-10 минут в зависимости от возраста)
        warm_up_duration = 5 if age_key in ["1-3", "3-6"] else 7 if age_key in ["6-9"] else 10
        warm_up = self._create_warm_up(age_group, warm_up_duration)
        activities.append(warm_up)

<<<<<<< HEAD
        # Основная часть (оставшееся время минус время на завершение)
        wrap_up_duration = 5 if age_key in ["1-3", "3-6"] else 8 if age_key in ["6-9"] else 10
        main_duration = duration - warm_up_duration - wrap_up_duration
        
        # Генерируем активности по фазам
        main_activities = self._create_adaptive_activities(
            theme, age_group, level, main_duration
=======
        # Основная часть (оставшееся время минус 5 минут на завершение)
        main_duration = duration - 10
        main_activities = self._create_main_activities(
            theme, age_group, main_duration
>>>>>>> origin/NIKITA
        )
        activities.extend(main_activities)

        # Завершение урока
        wrap_up = self._create_wrap_up(age_group, level, wrap_up_duration)
        activities.append(wrap_up)

        return activities

    def _generate_activities_with_template(
        self, theme: str, age_group: AgeGroup, level: EnglishLevel, duration: int, template: dict
    ) -> List[LessonActivity]:
        """Генерирует активности с использованием шаблона урока"""
        activities = []
        age_key = age_group.value
        
        # Получаем структуру из шаблона
        structure = template["structure"]
        
        # Разминка
        warm_up_duration = int(duration * structure.get("warm_up_ratio", 0.15))
        if warm_up_duration > 0:
            warm_up = self._create_warm_up(age_group, warm_up_duration)
            activities.append(warm_up)
        
        # Основная часть
        main_duration = duration - warm_up_duration - int(duration * structure.get("wrap_up_ratio", 0.1))
        
        # Введение лексики
        vocab_duration = int(main_duration * structure.get("vocabulary_ratio", 0.35))
        if vocab_duration > 0:
            vocab_activity = self._create_vocabulary_activity(theme, age_group, level, vocab_duration)
            activities.append(vocab_activity)
        
        # Практика
        practice_duration = int(main_duration * structure.get("practice_ratio", 0.35))
        if practice_duration > 0:
            practice_activities = self._create_practice_activities(theme, age_group, level, practice_duration)
            activities.extend(practice_activities)
        
        # Творческая активность
        creative_duration = int(main_duration * structure.get("creative_ratio", 0.15))
        if creative_duration > 0:
            creative_activity = self._create_creative_activity(theme, age_group, level, creative_duration)
            activities.append(creative_activity)
        
        # Завершение урока
        wrap_up_duration = duration - sum(activity.duration for activity in activities)
        if wrap_up_duration > 0:
            wrap_up = self._create_wrap_up(age_group, level, wrap_up_duration)
            activities.append(wrap_up)
        
        return activities

    def _create_warm_up(self, age_group: AgeGroup, duration: int) -> LessonActivity:
        """Создает разминку в зависимости от возраста"""
        age_key = age_group.value
        
        # Получаем шаблоны разминки из загруженных шаблонов
        warm_up_templates = self.activity_templates.get("warm_up", {})
        
        if age_key in warm_up_templates and warm_up_templates[age_key]:
            # Выбираем случайную активность из доступных
            import random
            template = random.choice(warm_up_templates[age_key])
            # Адаптируем длительность
            return LessonActivity(
                template.name,
                template.activity_type,
                duration,
                template.description,
                template.materials,
                template.instructions
            )
        
        # Fallback разминка
        if age_key in ["1-3", "3-6"]:
            return LessonActivity(
                "Музыкальная разминка",
                ActivityType.SONG,
                duration,
                "Простая песенка с движениями",
                ["аудиозапись", "игрушки"],
                ["Включить музыку", "Показать движения", "Петь вместе с детьми"],
            )
        else:
            return LessonActivity(
                "Быстрые вопросы",
                ActivityType.DIALOGUE,
                duration,
                "Вопрос-ответ для активизации речи",
                [],
                ["Задать простые вопросы", "Выслушать ответы", "Поправить при необходимости"],
            )

<<<<<<< HEAD
    def _create_adaptive_activities(
        self, theme: str, age_group: AgeGroup, level: EnglishLevel, duration: int
=======
    def _create_main_activities(
        self, theme: str, age_group: AgeGroup, duration: int
>>>>>>> origin/NIKITA
    ) -> List[LessonActivity]:
        """Создает адаптивные активности для основной части урока"""
        activities = []
        age_key = age_group.value
        level_key = level.value
        
        # Распределяем время между фазами урока
        time_distribution = self._calculate_time_distribution(age_key, level_key, duration)
        
        # 1. Введение лексики (30-40% времени)
        vocab_duration = time_distribution["vocabulary"]
        if vocab_duration > 0:
            vocab_activity = self._create_vocabulary_activity(theme, age_group, level, vocab_duration)
            activities.append(vocab_activity)
        
        # 2. Практика (40-50% времени)
        practice_duration = time_distribution["practice"]
        if practice_duration > 0:
            practice_activities = self._create_practice_activities(theme, age_group, level, practice_duration)
            activities.extend(practice_activities)
        
        # 3. Творческая активность (10-20% времени)
        creative_duration = time_distribution["creative"]
        if creative_duration > 0:
            creative_activity = self._create_creative_activity(theme, age_group, level, creative_duration)
            activities.append(creative_activity)
        
        return activities

    def _calculate_time_distribution(self, age_key: str, level_key: str, total_duration: int) -> dict:
        """Рассчитывает распределение времени между фазами урока"""
        if age_key in ["1-3", "3-6"]:
            # Для маленьких детей больше времени на введение лексики
            return {
                "vocabulary": int(total_duration * 0.5),
                "practice": int(total_duration * 0.3),
                "creative": int(total_duration * 0.2)
            }
        elif age_key in ["6-9"]:
            # Сбалансированное распределение
            return {
                "vocabulary": int(total_duration * 0.4),
                "practice": int(total_duration * 0.4),
                "creative": int(total_duration * 0.2)
            }
        else:
            # Для старших детей больше практики
            return {
                "vocabulary": int(total_duration * 0.3),
                "practice": int(total_duration * 0.5),
                "creative": int(total_duration * 0.2)
            }

    def _create_vocabulary_activity(
        self, theme: str, age_group: AgeGroup, level: EnglishLevel, duration: int
    ) -> LessonActivity:
        """Создает активность для изучения лексики"""
        age_key = age_group.value
        
        # Получаем шаблоны лексических активностей
        vocab_templates = self.activity_templates.get("vocabulary", {})
        
        if theme in vocab_templates and vocab_templates[theme]:
            import random
            template = random.choice(vocab_templates[theme])
            return LessonActivity(
                template.name,
                template.activity_type,
                duration,
                template.description,
                template.materials,
                template.instructions
            )
        
        # Fallback активность для изучения лексики
        return LessonActivity(
            f"Изучаем слова по теме '{theme}'",
            ActivityType.GAME,
            duration,
            f"Знакомство с новой лексикой по теме '{theme}'",
            ["карточки", "изображения", "аудиозаписи"],
            [
                "Показать карточки со словами",
                "Произнести слова четко",
                "Дети повторяют хором",
                "Использовать жесты и мимику",
                "Проверить понимание"
            ]
        )

    def _create_practice_activities(
        self, theme: str, age_group: AgeGroup, level: EnglishLevel, duration: int
    ) -> List[LessonActivity]:
        """Создает активности для практики"""
        activities = []
        age_key = age_group.value
        
        # Получаем шаблоны практических активностей
        practice_templates = self.activity_templates.get("practice", {})
        
        if age_key in practice_templates and practice_templates[age_key]:
            import random
            # Выбираем 1-2 активности в зависимости от времени
            num_activities = 1 if duration < 15 else 2
            selected_templates = random.sample(practice_templates[age_key], 
                                            min(num_activities, len(practice_templates[age_key])))
            
            for i, template in enumerate(selected_templates):
                activity_duration = duration // len(selected_templates)
                if i == len(selected_templates) - 1:  # Последняя активность получает оставшееся время
                    activity_duration = duration - (activity_duration * (len(selected_templates) - 1))
                
                activities.append(LessonActivity(
                    template.name,
                    template.activity_type,
                    activity_duration,
                    template.description,
                    template.materials,
                    template.instructions
                ))
        
        # Fallback активность для практики
        if not activities:
            activities.append(LessonActivity(
                "Практика изученного",
            ActivityType.GAME,
                duration,
                f"Закрепление материала по теме '{theme}'",
                ["игровые материалы", "карточки"],
                [
                    "Повторить изученные слова",
                    "Использовать их в играх",
                    "Поощрять активное участие",
                    "Проверить понимание"
                ]
            ))

        return activities

    def _create_creative_activity(
        self, theme: str, age_group: AgeGroup, level: EnglishLevel, duration: int
    ) -> LessonActivity:
        """Создает творческую активность"""
        age_key = age_group.value
        
        if age_key in ["1-3", "3-6"]:
            return LessonActivity(
                f"Рисуем {theme}",
                ActivityType.CRAFT,
                duration,
                f"Творческая активность по теме '{theme}'",
                ["бумага", "карандаши", "краски", "клей"],
                [
                    "Раздать материалы",
                    "Предложить нарисовать что-то по теме",
                    "Использовать английские слова",
                    "Похвалить за старание"
                ]
            )
        elif age_key in ["6-9"]:
            return LessonActivity(
                f"Создаем проект '{theme}'",
                ActivityType.CRAFT,
                duration,
                f"Создание творческого проекта по теме '{theme}'",
                ["бумага", "ножницы", "клей", "цветные карандаши"],
                [
                    "Объяснить задание",
                    "Раздать материалы",
                    "Помочь с выполнением",
                    "Презентовать результаты"
                ]
            )
        else:
            return LessonActivity(
                f"Презентация '{theme}'",
                ActivityType.CRAFT,
                duration,
                f"Создание презентации по теме '{theme}'",
                ["компьютеры", "принтер", "материалы"],
                [
                    "Выбрать подтему",
                    "Исследовать информацию",
                    "Создать презентацию",
                    "Представить классу"
                ]
            )

    def _create_wrap_up(self, age_group: AgeGroup, level: EnglishLevel, duration: int) -> LessonActivity:
        """Создает завершающую активность урока"""
        age_key = age_group.value
        
        if age_key in ["1-3", "3-6"]:
            return LessonActivity(
                "Прощание с игрушками",
                ActivityType.SONG,
                duration,
                "Веселое прощание с повторением изученного",
                ["игрушки", "музыка"],
                [
                    "Показать игрушки",
                    "Назвать их на английском",
                    "Спеть прощальную песенку",
                    "Похвалить детей"
                ]
            )
        elif age_key in ["6-9"]:
            return LessonActivity(
                "Повторение и закрепление",
                ActivityType.DIALOGUE,
                duration,
                "Повторение ключевых слов и фраз",
                ["карточки", "мелкие призы"],
                [
                    "Показать карточки",
                    "Дети называют слова",
                    "Задать вопросы по теме",
                    "Похвалить за работу"
                ]
            )
        else:
            return LessonActivity(
                "Рефлексия и обсуждение",
                ActivityType.DIALOGUE,
                duration,
                "Обсуждение урока и полученных знаний",
                ["листы рефлексии", "ручки"],
                [
                    "Спросить что понравилось",
                    "Что было сложным",
                    "Что запомнилось",
                    "Планы на следующий урок"
                ]
            )


    def _save_lesson(self, lesson: Lesson):
        filename = (
            f"{lesson.theme}_{lesson.age_group.value}_{lesson.en_level.value}.json"
        )
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
                    "instructions": activity.instructions,
                }
                for activity in lesson.activities
            ],
        }

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(lesson_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Урок сохранен в файл: {filename}")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")


class Person:
    def __init__(self, login, password, age, role):
        self.login = login
        self.password = password
        self.age = age
        self.role = role
