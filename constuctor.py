import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import db_service
import requests
import json

# --- Хранилище текущего пользователя ---
current_user = None

# --- DeepSeek API ---
DEEPSEEK_API_KEY = "sk-1dd84743d04d4a9a8865bd2678c374e6"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


def generate_tasks_with_ai(theme, age_group, vocabulary, duration):
    """Генерирует задания с помощью DeepSeek AI"""
    try:
        # Формируем промпт для AI
        prompt = f"""Ты - опытный преподаватель английского языка для детей.
        
Создай детальный план урока для учеников возраста {age_group} на тему "{theme}".
Длительность урока: {duration} минут.
Используй следующие слова из словаря: {', '.join(vocabulary[:10])}.

Верни ответ в формате JSON со следующей структурой:
{{
    "phases": [
        {{"name": "название фазы", "duration": время в минутах, "activities": ["активность 1", "активность 2"]}},
        ...
    ],
    "materials": ["материал 1", "материал 2", ...],
    "learning_objectives": ["цель 1", "цель 2", ...]
}}

Урок должен быть интерактивным, веселым и подходящим для возраста {age_group}.
Ответь ТОЛЬКО JSON, без дополнительного текста."""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are an expert English teacher for children. You always respond in Russian and provide structured lesson plans in JSON format."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Пытаемся извлечь JSON из ответа
            try:
                # Убираем markdown code blocks если есть
                if content.startswith('```'):
                    json_start = content.find('{')
                    json_end = content.rfind('}') + 1
                    content = content[json_start:json_end]
                
                ai_plan = json.loads(content)
                return ai_plan
            except (json.JSONDecodeError, KeyError):
                return None
        else:
            return None
    except Exception as e:
        print(f"Ошибка при работе с DeepSeek API: {e}")
        return None


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
    def __init__(self, theme, age_group, level, duration, use_ai=True):
        self.theme = theme
        self.age_group = age_group
        self.level = level
        self.duration = duration
        self.use_ai = use_ai
        self.vocabulary = self._generate_vocabulary()
        self.tasks = self._generate_tasks()
        self.ai_plan = None
        
        # Пытаемся получить план от AI если включено
        if self.use_ai and self.vocabulary:
            self.ai_plan = generate_tasks_with_ai(self.theme, self.age_group, self.vocabulary, self.duration)

    def _generate_vocabulary(self):
        """Генерирует словарь по теме"""
        vocab_dict = {
            "животные": {
                "1-3": ["cat", "dog", "bird"],
                "4-7": ["cat", "dog", "bird", "fish", "rabbit", "lion"],
                "8-15": ["cat", "dog", "bird", "fish", "rabbit", "lion", "elephant", "tiger", "bear", "monkey"]
            },
            "цвета": {
                "1-3": ["red", "blue", "yellow"],
                "4-7": ["red", "blue", "yellow", "green", "orange", "purple"],
                "8-15": ["red", "blue", "yellow", "green", "orange", "purple", "pink", "brown", "black", "white"]
            },
            "семья": {
                "1-3": ["mom", "dad", "baby"],
                "4-7": ["mom", "dad", "baby", "sister", "brother", "grandma"],
                "8-15": ["mom", "dad", "baby", "sister", "brother", "grandma", "grandpa", "aunt", "uncle", "cousin"]
            },
            "еда": {
                "1-3": ["apple", "banana", "milk"],
                "4-7": ["apple", "banana", "milk", "bread", "juice", "cake"],
                "8-15": ["apple", "banana", "milk", "bread", "juice", "cake", "pizza", "chicken", "rice", "soup"]
            },
            "одежда": {
                "1-3": ["hat", "shoes", "dress"],
                "4-7": ["hat", "shoes", "dress", "shirt", "pants", "socks"],
                "8-15": ["hat", "shoes", "dress", "shirt", "pants", "socks", "jacket", "skirt", "tie", "gloves"]
            },
            "дом": {
                "1-3": ["house", "bed", "table"],
                "4-7": ["house", "bed", "table", "chair", "window", "door"],
                "8-15": ["house", "bed", "table", "chair", "window", "door", "kitchen", "bathroom", "garden", "garage"]
            },
            "школа": {
                "1-3": ["book", "pen", "bag"],
                "4-7": ["book", "pen", "bag", "pencil", "ruler", "eraser"],
                "8-15": ["book", "pen", "bag", "pencil", "ruler", "eraser", "notebook", "calculator", "computer", "desk"]
            },
            "хобби": {
                "1-3": ["play", "sing", "draw"],
                "4-7": ["play", "sing", "draw", "dance", "swim", "run"],
                "8-15": ["play", "sing", "draw", "dance", "swim", "run", "read", "write", "cook", "travel"]
            },
            "части тела": {
                "1-3": ["head", "eyes", "nose"],
                "4-7": ["head", "eyes", "nose", "mouth", "hands", "feet"],
                "8-15": ["head", "eyes", "nose", "mouth", "hands", "feet", "arms", "legs", "ears", "hair"]
            },
            "игрушки": {
                "1-3": ["ball", "doll", "car"],
                "4-7": ["ball", "doll", "car", "teddy", "blocks", "puzzle"],
                "8-15": ["ball", "doll", "car", "teddy", "blocks", "puzzle", "robot", "game", "toy", "kite"]
            }
        }
        return vocab_dict.get(self.theme, {}).get(self.age_group, [])

    def _generate_tasks(self):
        """Генерирует конкретные задания по теме и возрасту"""
        tasks_dict = {
            "животные": {
                "1-3": [
                    {
                        "type": "Игра 'Звуки животных'",
                        "description": "Покажите карточку с животным и произнесите звук",
                        "example": "Покажите кошку → 'Meow-meow!'",
                        "solution": "Дети повторяют звуки и показывают на карточки"
                    },
                    {
                        "type": "Игра 'Найди животное'",
                        "description": "Спрячьте карточки и попросите найти",
                        "example": "Where is the cat? → Дети ищут карточку с кошкой",
                        "solution": "Покажите карточку и скажите 'Here is the cat!'"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Животные и их дома'",
                        "description": "Соедините животных с их домами",
                        "example": "Dog lives in a house. Bird lives in a tree.",
                        "solution": "Покажите картинки и объясните где живут животные"
                    },
                    {
                        "type": "Песня 'Old MacDonald'",
                        "description": "Спойте песню с животными",
                        "example": "Old MacDonald had a farm, E-I-E-I-O!",
                        "solution": "Дети поют и показывают движения животных"
                    },
                    {
                        "type": "Игра 'Угадай животное'",
                        "description": "Опишите животное, дети угадывают",
                        "example": "It's big, it's gray, it has a trunk. What is it?",
                        "solution": "It's an elephant!"
                    }
                ],
                "8-15": [
                    {
                        "type": "Диалог 'В зоопарке'",
                        "description": "Составьте диалог между посетителями зоопарка",
                        "example": "A: Look! What's that? B: It's a lion. A: Is it dangerous?",
                        "solution": "Предложите готовый диалог и попросите повторить"
                    },
                    {
                        "type": "Проект 'Мое любимое животное'",
                        "description": "Расскажите о своем любимом животном",
                        "example": "My favorite animal is a dog because it's friendly.",
                        "solution": "Помогите составить рассказ из 3-5 предложений"
                    },
                    {
                        "type": "Игра 'Животные разных стран'",
                        "description": "Назовите животных из разных стран",
                        "example": "Kangaroo is from Australia. Panda is from China.",
                        "solution": "Покажите карту мира и разместите животных по странам"
                    }
                ]
            },
            "цвета": {
                "1-3": [
                    {
                        "type": "Игра 'Покажи цвет'",
                        "description": "Покажите предмет определенного цвета",
                        "example": "Show me something red!",
                        "solution": "Дети показывают красные предметы в комнате"
                    },
                    {
                        "type": "Раскраска",
                        "description": "Раскрасьте картинку по инструкции",
                        "example": "Color the apple red, color the sun yellow",
                        "solution": "Проверьте правильность раскрашивания"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Цвета и предметы'",
                        "description": "Назовите предметы определенного цвета",
                        "example": "What is red? → Apple, rose, fire truck",
                        "solution": "Составьте список предметов каждого цвета"
                    },
                    {
                        "type": "Эксперимент 'Смешивание цветов'",
                        "description": "Смешайте краски и назовите новый цвет",
                        "example": "Red + Blue = Purple",
                        "solution": "Покажите таблицу смешивания цветов"
                    },
                    {
                        "type": "Песня 'Rainbow Song'",
                        "description": "Спойте песню о радуге",
                        "example": "Red and yellow and pink and green...",
                        "solution": "Дети поют и показывают цвета руками"
                    }
                ],
                "8-15": [
                    {
                        "type": "Описание картины",
                        "description": "Опишите картину используя цвета",
                        "example": "The sky is blue, the grass is green, the flowers are colorful",
                        "solution": "Предложите шаблон описания с прилагательными"
                    },
                    {
                        "type": "Игра 'Цветовые ассоциации'",
                        "description": "Скажите с чем ассоциируется цвет",
                        "example": "Red makes me think of love and fire",
                        "solution": "Обсудите эмоциональные ассоциации цветов"
                    },
                    {
                        "type": "Проект 'Цвета в природе'",
                        "description": "Найдите цвета в природе и опишите их",
                        "example": "Autumn leaves are orange and brown",
                        "solution": "Создайте коллаж из природных материалов"
                    }
                ]
            },
            "семья": {
                "1-3": [
                    {
                        "type": "Игра 'Покажи семью'",
                        "description": "Покажите на картинке членов семьи",
                        "example": "Where is mommy? Where is daddy?",
                        "solution": "Дети показывают пальцем на картинки"
                    },
                    {
                        "type": "Песня 'Family Finger Song'",
                        "description": "Спойте песню про пальчики семьи",
                        "example": "Daddy finger, daddy finger, where are you?",
                        "solution": "Дети показывают пальцы и поют"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Семейное дерево'",
                        "description": "Постройте семейное дерево",
                        "example": "Grandma and Grandpa are at the top, Mom and Dad are below",
                        "solution": "Покажите схему семейного дерева"
                    },
                    {
                        "type": "Диалог 'Расскажи о семье'",
                        "description": "Расскажите о своей семье",
                        "example": "I have a mom, a dad, and a sister",
                        "solution": "Помогите составить простое предложение"
                    },
                    {
                        "type": "Игра 'Семейные роли'",
                        "description": "Покажите кто что делает в семье",
                        "example": "Mom cooks dinner. Dad drives the car.",
                        "solution": "Обсудите обязанности каждого члена семьи"
                    }
                ],
                "8-15": [
                    {
                        "type": "Интервью с семьей",
                        "description": "Возьмите интервью у члена семьи",
                        "example": "What's your favorite hobby? What do you like to do?",
                        "solution": "Составьте список вопросов для интервью"
                    },
                    {
                        "type": "Проект 'Семейная история'",
                        "description": "Расскажите историю своей семьи",
                        "example": "My family came from Russia. We moved here 5 years ago.",
                        "solution": "Помогите составить рассказ о семейной истории"
                    },
                    {
                        "type": "Дебаты 'Семейные традиции'",
                        "description": "Обсудите важность семейных традиций",
                        "example": "Family traditions help us stay connected",
                        "solution": "Подготовьте аргументы за и против"
                    }
                ]
            },
            "еда": {
                "1-3": [
                    {
                        "type": "Игра 'Вкусная еда'",
                        "description": "Покажите карточки с едой и скажите вкусно",
                        "example": "Show apple → 'Yummy!'",
                        "solution": "Дети повторяют 'Yummy!' и показывают на карточки"
                    },
                    {
                        "type": "Игра 'Кормление куклы'",
                        "description": "Покормите куклу разной едой",
                        "example": "Feed the doll an apple",
                        "solution": "Дети берут карточки с едой и 'кормят' куклу"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Что я ем'",
                        "description": "Опишите еду, дети угадывают",
                        "example": "It's yellow, it's sweet, monkeys love it. What is it?",
                        "solution": "It's a banana!"
                    },
                    {
                        "type": "Песня 'Apples and Bananas'",
                        "description": "Спойте песню про фрукты",
                        "example": "I like to eat, eat, eat apples and bananas",
                        "solution": "Дети поют и показывают движения"
                    },
                    {
                        "type": "Игра 'Здоровое питание'",
                        "description": "Разделите еду на здоровую и нездоровую",
                        "example": "Apple is healthy. Candy is not healthy",
                        "solution": "Создайте две корзины для сортировки"
                    }
                ],
                "8-15": [
                    {
                        "type": "Диалог 'В ресторане'",
                        "description": "Составьте диалог заказа еды",
                        "example": "A: What would you like? B: I'd like pizza, please",
                        "solution": "Предложите меню и фразы для заказа"
                    },
                    {
                        "type": "Проект 'Мой любимый рецепт'",
                        "description": "Расскажите о любимом блюде",
                        "example": "My favorite food is pasta because it's delicious",
                        "solution": "Помогите составить рецепт на английском"
                    },
                    {
                        "type": "Дебаты 'Здоровое питание'",
                        "description": "Обсудите важность здорового питания",
                        "example": "Healthy food gives us energy",
                        "solution": "Подготовьте аргументы за здоровое питание"
                    }
                ]
            },
            "одежда": {
                "1-3": [
                    {
                        "type": "Игра 'Одень куклу'",
                        "description": "Оденьте куклу в разную одежду",
                        "example": "Put on the hat",
                        "solution": "Дети одевают куклу по инструкции"
                    },
                    {
                        "type": "Игра 'Покажи одежду'",
                        "description": "Покажите на себе предметы одежды",
                        "example": "Show me your shoes",
                        "solution": "Дети показывают на свою одежду"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Одежда по сезонам'",
                        "description": "Выберите одежду для разных сезонов",
                        "example": "Winter: coat, hat, gloves. Summer: dress, shorts",
                        "solution": "Создайте корзины для каждого сезона"
                    },
                    {
                        "type": "Песня 'Put On Your Shoes'",
                        "description": "Спойте песню про одевание",
                        "example": "Put on your shoes, your shoes, your shoes",
                        "solution": "Дети поют и показывают движения одевания"
                    },
                    {
                        "type": "Игра 'Опиши одежду'",
                        "description": "Опишите одежду по цвету и размеру",
                        "example": "It's a big red shirt",
                        "solution": "Дети угадывают предмет одежды"
                    }
                ],
                "8-15": [
                    {
                        "type": "Диалог 'Покупка одежды'",
                        "description": "Составьте диалог в магазине одежды",
                        "example": "A: Can I help you? B: I'm looking for a blue shirt",
                        "solution": "Предложите фразы для покупки одежды"
                    },
                    {
                        "type": "Проект 'Модный показ'",
                        "description": "Организуйте модный показ",
                        "example": "This is my favorite outfit for school",
                        "solution": "Помогите описать наряд на английском"
                    },
                    {
                        "type": "Игра 'Одежда разных стран'",
                        "description": "Расскажите о традиционной одежде",
                        "example": "In Japan people wear kimonos",
                        "solution": "Покажите картинки традиционной одежды"
                    }
                ]
            },
            "дом": {
                "1-3": [
                    {
                        "type": "Игра 'Дом для куклы'",
                        "description": "Постройте дом из кубиков",
                        "example": "Put the bed in the bedroom",
                        "solution": "Дети строят дом по инструкции"
                    },
                    {
                        "type": "Игра 'Где что лежит'",
                        "description": "Найдите предметы в доме",
                        "example": "Where is the book? → In the bedroom",
                        "solution": "Дети показывают на картинки комнат"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Комнаты дома'",
                        "description": "Назовите комнаты и что в них",
                        "example": "Kitchen: stove, fridge, table",
                        "solution": "Создайте план дома с комнатами"
                    },
                    {
                        "type": "Песня 'My House'",
                        "description": "Спойте песню про дом",
                        "example": "This is my house, this is my door",
                        "solution": "Дети поют и показывают части дома"
                    },
                    {
                        "type": "Игра 'Мебель и предметы'",
                        "description": "Соедините предметы с комнатами",
                        "example": "Bed goes in bedroom, stove goes in kitchen",
                        "solution": "Создайте карточки для сортировки"
                    }
                ],
                "8-15": [
                    {
                        "type": "Диалог 'Описание дома'",
                        "description": "Опишите свой дом",
                        "example": "My house has three bedrooms and a big kitchen",
                        "solution": "Помогите составить описание дома"
                    },
                    {
                        "type": "Проект 'Идеальный дом'",
                        "description": "Спроектируйте идеальный дом",
                        "example": "My dream house has a swimming pool",
                        "solution": "Создайте план дома на английском"
                    },
                    {
                        "type": "Игра 'Дома разных стран'",
                        "description": "Сравните дома в разных странах",
                        "example": "In England houses are made of brick",
                        "solution": "Покажите картинки домов разных стран"
                    }
                ]
            },
            "школа": {
                "1-3": [
                    {
                        "type": "Игра 'Школьные предметы'",
                        "description": "Покажите школьные принадлежности",
                        "example": "Show me the book",
                        "solution": "Дети показывают на школьные предметы"
                    },
                    {
                        "type": "Игра 'Собери портфель'",
                        "description": "Соберите портфель для школы",
                        "example": "Put the book in the bag",
                        "solution": "Дети собирают портфель по инструкции"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Школьные предметы'",
                        "description": "Назовите предметы и их назначение",
                        "example": "We use pencil to write, we use ruler to measure",
                        "solution": "Объясните назначение каждого предмета"
                    },
                    {
                        "type": "Песня 'School Supplies Song'",
                        "description": "Спойте песню про школьные принадлежности",
                        "example": "I have a pencil, I have a pen",
                        "solution": "Дети поют и показывают предметы"
                    },
                    {
                        "type": "Игра 'Что в портфеле'",
                        "description": "Опишите что лежит в портфеле",
                        "example": "In my bag I have books, pencils, and an eraser",
                        "solution": "Дети перечисляют предметы в портфеле"
                    }
                ],
                "8-15": [
                    {
                        "type": "Диалог 'В школе'",
                        "description": "Составьте диалог между учениками",
                        "example": "A: Can I borrow your pen? B: Sure, here you are",
                        "solution": "Предложите фразы для общения в школе"
                    },
                    {
                        "type": "Проект 'Мой школьный день'",
                        "description": "Расскажите о своем школьном дне",
                        "example": "I go to school at 8 o'clock",
                        "solution": "Помогите составить расписание дня"
                    },
                    {
                        "type": "Игра 'Школы разных стран'",
                        "description": "Сравните школы в разных странах",
                        "example": "In Japan students clean their classrooms",
                        "solution": "Покажите особенности школ разных стран"
                    }
                ]
            },
            "хобби": {
                "1-3": [
                    {
                        "type": "Игра 'Что я люблю делать'",
                        "description": "Покажите любимые занятия",
                        "example": "I like to play",
                        "solution": "Дети показывают движения игр"
                    },
                    {
                        "type": "Игра 'Песни и танцы'",
                        "description": "Спойте и станцуйте",
                        "example": "Let's sing and dance together",
                        "solution": "Дети поют и танцуют под музыку"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Мои хобби'",
                        "description": "Расскажите о своих увлечениях",
                        "example": "I like to draw pictures",
                        "solution": "Дети рисуют и рассказывают о рисунке"
                    },
                    {
                        "type": "Песня 'Hobbies Song'",
                        "description": "Спойте песню про хобби",
                        "example": "I like to read, I like to play",
                        "solution": "Дети поют и показывают свои хобби"
                    },
                    {
                        "type": "Игра 'Угадай хобби'",
                        "description": "Опишите хобби, дети угадывают",
                        "example": "I use brushes and paint. What is my hobby?",
                        "solution": "It's painting!"
                    }
                ],
                "8-15": [
                    {
                        "type": "Диалог 'О хобби'",
                        "description": "Обсудите хобби с друзьями",
                        "example": "A: What's your hobby? B: I like playing football",
                        "solution": "Предложите фразы для обсуждения хобби"
                    },
                    {
                        "type": "Проект 'Мое хобби'",
                        "description": "Создайте презентацию о своем хобби",
                        "example": "My hobby is photography. I take pictures of nature",
                        "solution": "Помогите составить презентацию на английском"
                    },
                    {
                        "type": "Игра 'Хобби знаменитостей'",
                        "description": "Расскажите о хобби известных людей",
                        "example": "Einstein liked playing violin",
                        "solution": "Покажите интересные факты о хобби знаменитостей"
                    }
                ]
            },
            "части тела": {
                "1-3": [
                    {
                        "type": "Игра 'Покажи части тела'",
                        "description": "Покажите на себе части тела",
                        "example": "Show me your nose",
                        "solution": "Дети показывают на свои части тела"
                    },
                    {
                        "type": "Песня 'Head, Shoulders, Knees and Toes'",
                        "description": "Спойте песню про части тела",
                        "example": "Head, shoulders, knees and toes",
                        "solution": "Дети поют и показывают на части тела"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Одень куклу'",
                        "description": "Оденьте куклу и назовите части тела",
                        "example": "Put shoes on feet, hat on head",
                        "solution": "Дети одевают куклу и называют части тела"
                    },
                    {
                        "type": "Игра 'Угадай часть тела'",
                        "description": "Опишите часть тела, дети угадывают",
                        "example": "We use it to smell. What is it?",
                        "solution": "It's a nose!"
                    }
                ],
                "8-15": [
                    {
                        "type": "Диалог 'У врача'",
                        "description": "Составьте диалог с врачом",
                        "example": "A: What's wrong? B: My head hurts",
                        "solution": "Предложите фразы для описания боли"
                    },
                    {
                        "type": "Проект 'Человеческое тело'",
                        "description": "Опишите функции частей тела",
                        "example": "The heart pumps blood through the body",
                        "solution": "Помогите составить описание функций органов"
                    }
                ]
            },
            "игрушки": {
                "1-3": [
                    {
                        "type": "Игра 'Мои игрушки'",
                        "description": "Покажите любимые игрушки",
                        "example": "This is my teddy bear",
                        "solution": "Дети приносят игрушки и показывают их"
                    },
                    {
                        "type": "Игра 'Спрячь игрушку'",
                        "description": "Спрячьте игрушку и попросите найти",
                        "example": "Where is the ball?",
                        "solution": "Дети ищут спрятанную игрушку"
                    }
                ],
                "4-7": [
                    {
                        "type": "Игра 'Опиши игрушку'",
                        "description": "Опишите игрушку по цвету и размеру",
                        "example": "It's a big red car",
                        "solution": "Дети угадывают игрушку по описанию"
                    },
                    {
                        "type": "Песня 'Toys Song'",
                        "description": "Спойте песню про игрушки",
                        "example": "I have a ball, I have a doll",
                        "solution": "Дети поют и показывают свои игрушки"
                    }
                ],
                "8-15": [
                    {
                        "type": "Диалог 'В магазине игрушек'",
                        "description": "Составьте диалог покупки игрушки",
                        "example": "A: How much is this toy? B: It's 20 dollars",
                        "solution": "Предложите фразы для покупки"
                    },
                    {
                        "type": "Проект 'Моя любимая игрушка'",
                        "description": "Расскажите о любимой игрушке",
                        "example": "My favorite toy is a robot because it can move",
                        "solution": "Помогите составить рассказ об игрушке"
                    }
                ]
            }
        }
        
        # Получаем задания для конкретной темы и возраста
        theme_tasks = tasks_dict.get(self.theme, {})
        age_tasks = theme_tasks.get(self.age_group, [])
        
        # Если нет заданий для конкретного возраста, берем ближайший
        if not age_tasks:
            if self.age_group == "1-3":
                age_tasks = theme_tasks.get("4-7", [])
            elif self.age_group == "4-7":
                age_tasks = theme_tasks.get("8-15", [])
            else:
                age_tasks = theme_tasks.get("4-7", [])
        
        return age_tasks[:3]  # Возвращаем максимум 3 задания

    def get_lesson_plan(self):
        plan = f"🎓 ПЛАН УРОКА\n"
        plan += f"Тема: {self.theme.title()}\n"
        plan += f"Возраст: {self.age_group}\n"
        plan += f"Длительность: {self.duration} минут\n"
        
        # Если есть план от AI, используем его
        if self.ai_plan:
            plan += f"\n🤖 Сгенерировано с помощью AI\n"
            
            # Цели обучения
            if "learning_objectives" in self.ai_plan:
                plan += f"\n🎯 ЦЕЛИ УРОКА:\n"
                for obj in self.ai_plan["learning_objectives"]:
                    plan += f"• {obj}\n"
            
            # Фазы урока
            if "phases" in self.ai_plan:
                plan += f"\n⏰ ФАЗЫ УРОКА:\n"
                for phase in self.ai_plan["phases"]:
                    phase_name = phase.get("name", "Фаза")
                    phase_duration = phase.get("duration", "")
                    activities = phase.get("activities", [])
                    
                    plan += f"\n• {phase_name} ({phase_duration} мин)\n"
                    for activity in activities:
                        plan += f"  - {activity}\n"
            
            # Словарь
            plan += f"\n📚 СЛОВАРЬ ({len(self.vocabulary)} слов):\n"
            for word in self.vocabulary:
                plan += f"• {word}\n"
            
            # Материалы
            if "materials" in self.ai_plan:
                plan += f"\n📦 МАТЕРИАЛЫ:\n"
                for material in self.ai_plan["materials"]:
                    plan += f"• {material}\n"
            else:
                plan += f"\n📦 МАТЕРИАЛЫ:\n"
                plan += f"• Карточки со словами по теме '{self.theme}'\n"
                plan += f"• Раскраски и рабочие листы\n"
                plan += f"• Аудиозаписи и песни\n"
                plan += f"• Игрушки и предметы для демонстрации\n"
        
        else:
            # Используем заготовленные задания
            phases = {
                30: ["Разминка (3 мин)", "Изучение лексики (12 мин)", "Задания (10 мин)", "Завершение (5 мин)"],
                45: ["Разминка (5 мин)", "Изучение лексики (15 мин)", "Задания (20 мин)", "Завершение (5 мин)"],
                60: ["Разминка (10 мин)", "Изучение лексики (20 мин)", "Задания (25 мин)", "Завершение (5 мин)"],
                90: ["Разминка (10 мин)", "Изучение лексики (25 мин)", "Задания (45 мин)", "Завершение (10 мин)"]
            }
            
            plan += f"\n📚 СЛОВАРЬ ({len(self.vocabulary)} слов):\n"
            for word in self.vocabulary:
                plan += f"• {word}\n"
            
            plan += f"\n⏰ ФАЗЫ УРОКА:\n"
        for phase in phases.get(self.duration, phases[45]):
            plan += f"• {phase}\n"
            
            plan += f"\n🎯 КОНКРЕТНЫЕ ЗАДАНИЯ:\n"
            for i, task in enumerate(self.tasks, 1):
                plan += f"\n{i}. {task['type']}\n"
                plan += f"   📝 Описание: {task['description']}\n"
                plan += f"   💡 Пример: {task['example']}\n"
                plan += f"   ✅ Решение: {task['solution']}\n"
            
            plan += f"\n📦 МАТЕРИАЛЫ:\n"
            plan += f"• Карточки со словами по теме '{self.theme}'\n"
            plan += f"• Раскраски и рабочие листы\n"
            plan += f"• Аудиозаписи и песни\n"
            plan += f"• Игрушки и предметы для демонстрации\n"
        
        return plan


# --- Конструктор занятий ---
def Constructor(parent_window=None):
    win = tk.Toplevel()
    win.title("Конструктор уроков")
    win.geometry("800x750")
    win.resizable(False, False)
    win.configure(bg="#fffacd")  # Бледно-желтый фон

    # Центрируем окно
    center_window(win)

    # Заголовок с зеленым фоном
    header_frame = tk.Frame(win, bg="#4CAF50", height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    # Кнопка "Назад" в левом углу
    def go_back():
        win.destroy()
        if parent_window:
            parent_window.deiconify()  # Показываем родительское окно обратно
    
    back_btn = tk.Button(header_frame, text="← Назад", font=("Arial", 10, "bold"),
                        bg="#2E7D32", fg="white", width=8, height=1,
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#1B5E20", command=go_back)
    back_btn.place(x=10, y=25)
    
    tk.Label(header_frame, text="🎓 Конструктор уроков", 
             font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)

    frame = tk.Frame(win, bg="#fffacd", padx=20, pady=20)  # Бледно-желтый фон
    frame.pack(fill="both", expand=True)

    # Возрастная группа (первая)
    tk.Label(frame, text="Возрастная группа:", font=("Arial", 12, "bold"), bg="#fffacd", fg="#2e7d32").grid(row=0, column=0, sticky="w", pady=10)
    age_var = tk.StringVar()
    age_combo = ttk.Combobox(frame, textvariable=age_var, values=["Дети 1-3 года", "Дошкольники 4-7 лет", "Школьники 8-15 лет"], width=30, state="readonly")
    age_combo.grid(row=0, column=1)

    # Тема урока (вторая, зависит от возраста)
    tk.Label(frame, text="Тема урока:", font=("Arial", 12, "bold"), bg="#fffacd", fg="#2e7d32").grid(row=1, column=0, sticky="w", pady=10)
    theme_var = tk.StringVar()
    theme_combo = ttk.Combobox(frame, textvariable=theme_var, width=30, state="readonly")
    theme_combo.grid(row=1, column=1)

    # Длительность (третья)
    tk.Label(frame, text="Длительность (мин):", font=("Arial", 12, "bold"), bg="#fffacd", fg="#2e7d32").grid(row=2, column=0, sticky="w", pady=10)
    duration_var = tk.StringVar(value="45")
    duration_combo = ttk.Combobox(frame, textvariable=duration_var, values=["30", "45", "60", "90"], width=30, state="readonly")
    duration_combo.grid(row=2, column=1)

    # Область вывода
    tk.Label(frame, text="План урока:", font=("Arial", 12, "bold"), bg="#fffacd", fg="#2e7d32").grid(row=4, column=0, columnspan=2, sticky="w", pady=10)
    output = scrolledtext.ScrolledText(frame, width=70, height=20, font=("Courier", 10), bg="#ffffff", fg="#333333")
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

    # Переменная для хранения текущего урока
    current_lesson_data = {"lesson": None, "theme": "", "age_group": "", "duration": 0}

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

            # Показываем индикатор загрузки
            output.delete("1.0", tk.END)
            output.insert("1.0", "🔄 Генерирую план урока...\nПожалуйста, подождите...")
            win.update()

            # Используем фиксированный уровень (beginner) для всех уроков
            # AI включен по умолчанию
            lesson = ConsoleLessonBuilder()._generate_lesson(theme, age_map[age_str], duration)
            
            # Сохраняем данные урока
            current_lesson_data["lesson"] = lesson
            current_lesson_data["theme"] = theme
            current_lesson_data["age_group"] = age_str
            current_lesson_data["duration"] = duration
            
            output.delete("1.0", tk.END)
            output.insert("1.0", lesson.get_lesson_plan())
            
            # Включаем кнопку сохранения
            save_lesson_btn.config(state="normal")
            
            if lesson.ai_plan:
                messagebox.showinfo("Готово", "Детальный урок успешно создан с помощью AI! 🤖")
            else:
                messagebox.showinfo("Готово", "Урок успешно создан!")
        except ValueError as ve:
            messagebox.showerror("Ошибка", f"Некорректное значение: {ve}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    # Кнопки
    button_frame = tk.Frame(frame, bg="#fffacd")
    button_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10)
    
    tk.Button(button_frame, text="Создать урок", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
              width=15, height=2, command=create_lesson, relief="flat", bd=0, cursor="hand2",
              activebackground="#45a049").pack(side="left", padx=5)
    
    # Кнопка сохранения (появится только после создания урока)
    save_lesson_btn = tk.Button(button_frame, text="💾 Сохранить урок", font=("Arial", 12, "bold"), 
                                bg="#2196F3", fg="white", width=15, height=2, 
                                relief="flat", bd=0, cursor="hand2",
                                activebackground="#1976D2", state="disabled")
    save_lesson_btn.pack(side="left", padx=5)
    
    def save_current_lesson():
        if not current_lesson_data["lesson"]:
            messagebox.showwarning("Предупреждение", "Сначала создайте урок")
            return
        
        if not current_user:
            messagebox.showwarning("Предупреждение", "Вы не авторизованы")
            return
        
        try:
            title = f"{current_lesson_data['theme']} ({current_lesson_data['age_group']})"
            lesson_plan = current_lesson_data["lesson"].get_lesson_plan()
            
            db_service.db_save_lesson(
                title=title,
                theme=current_lesson_data["theme"],
                age_group=current_lesson_data["age_group"],
                duration=current_lesson_data["duration"],
                lesson_plan=lesson_plan,
                created_by=current_user.get("login")
            )
            
            messagebox.showinfo("Успех", "Урок успешно сохранен!")
            save_lesson_btn.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить урок: {e}")
    
    save_lesson_btn.config(command=save_current_lesson)


# --- Окно сохраненных уроков ---
def show_saved_lessons_window(root_parent=None):
    """Показать все сохраненные уроки"""
    if root_parent:
        root_parent.withdraw()
    
    lessons_win = tk.Tk()
    lessons_win.title("Сохраненные уроки")
    lessons_win.geometry("900x700")
    lessons_win.resizable(False, False)
    lessons_win.configure(bg="#fffacd")
    
    center_window(lessons_win)
    
    # Заголовок
    header_frame = tk.Frame(lessons_win, bg="#4CAF50", height=100)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    def go_back():
        lessons_win.destroy()
        if root_parent:
            root_parent.deiconify()
    
    back_btn = tk.Button(header_frame, text="← Назад", font=("Arial", 10, "bold"),
                        bg="#2E7D32", fg="white", width=8, height=1,
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#1B5E20", command=go_back)
    back_btn.place(x=10, y=35)
    
    tk.Label(header_frame, text="📚 Сохраненные уроки", 
             font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=25)
    
    # Контейнер для списка уроков
    main_container = tk.Frame(lessons_win, bg="#fffacd", padx=20, pady=20)
    main_container.pack(fill="both", expand=True)
    
    # Получаем все сохраненные уроки
    lessons = db_service.db_get_all_lessons()
    
    if not lessons:
        # Нет сохраненных уроков
        no_lessons_frame = tk.Frame(main_container, bg="#e8f5e9", relief="solid", bd=1, padx=30, pady=30)
        no_lessons_frame.pack(fill="both", expand=True, pady=100)
        
        tk.Label(no_lessons_frame, text="📝 Нет сохраненных уроков", 
                font=("Arial", 18, "bold"), bg="#e8f5e9", fg="#555").pack(pady=20)
        
        tk.Label(no_lessons_frame, text="Создайте уроки в конструкторе и сохраните их", 
                font=("Arial", 12), bg="#e8f5e9", fg="#777").pack(pady=10)
    else:
        # Создаем scrolled frame для списка уроков
        canvas = tk.Canvas(main_container, bg="#fffacd", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#fffacd")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Функция для просмотра урока
        def view_lesson(lesson_id):
            lesson_plan = db_service.db_get_lesson_by_id(lesson_id)
            if lesson_plan:
                view_window = tk.Toplevel(lessons_win)
                view_window.title("План урока")
                view_window.geometry("800x600")
                view_window.configure(bg="#fffacd")
                
                # Заголовок
                view_header = tk.Frame(view_window, bg="#4CAF50", height=60)
                view_header.pack(fill="x")
                view_header.pack_propagate(False)
                tk.Label(view_header, text="📄 План урока", 
                        font=("Arial", 18, "bold"), bg="#4CAF50", fg="white").pack(pady=15)
                
                # Контент
                view_content = scrolledtext.ScrolledText(view_window, width=90, height=30, 
                                                         font=("Courier", 10), bg="#ffffff", 
                                                         fg="#333333")
                view_content.pack(fill="both", expand=True, padx=20, pady=20)
                view_content.insert("1.0", lesson_plan)
                view_content.config(state="disabled")
                
                # Кнопка закрыть
                tk.Button(view_window, text="❌ Закрыть", font=("Arial", 12, "bold"),
                          bg="#D32F2F", fg="white", width=15, height=2,
                          activebackground="#C62828", relief="flat", bd=0, cursor="hand2",
                          command=view_window.destroy).pack(pady=10)
        
        # Функция для редактирования урока
        def edit_lesson(lesson_id):
            full_lesson = db_service.db_get_full_lesson_by_id(lesson_id)
            if not full_lesson:
                messagebox.showerror("Ошибка", "Урок не найден")
                return
            
            edit_window = tk.Toplevel(lessons_win)
            edit_window.title("Редактирование урока")
            edit_window.geometry("900x750")
            edit_window.configure(bg="#fffacd")
            center_window(edit_window)
            
            # Заголовок
            edit_header = tk.Frame(edit_window, bg="#4CAF50", height=80)
            edit_header.pack(fill="x")
            edit_header.pack_propagate(False)
            tk.Label(edit_header, text="✏️ Редактирование урока", 
                    font=("Arial", 18, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
            
            # Основной контейнер
            main_edit_frame = tk.Frame(edit_window, bg="#fffacd")
            main_edit_frame.pack(fill="both", expand=True)
            
            # Контейнер для скролла
            scroll_frame = tk.Frame(main_edit_frame, bg="#fffacd")
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            canvas_edit = tk.Canvas(scroll_frame, bg="#fffacd", highlightthickness=0)
            scrollbar_edit = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas_edit.yview)
            edit_content = tk.Frame(canvas_edit, bg="#fffacd", padx=20, pady=15)
            
            edit_content.bind(
                "<Configure>",
                lambda e: canvas_edit.configure(scrollregion=canvas_edit.bbox("all"))
            )
            
            canvas_edit.create_window((0, 0), window=edit_content, anchor="nw")
            canvas_edit.configure(yscrollcommand=scrollbar_edit.set)
            
            canvas_edit.pack(side="left", fill="both", expand=True)
            scrollbar_edit.pack(side="right", fill="y")
            
            # Тема
            tk.Label(edit_content, text="Тема урока:", font=("Arial", 11, "bold"), 
                    bg="#fffacd", fg="#2e7d32").pack(anchor="w", pady=5)
            theme_entry = tk.Entry(edit_content, width=50, font=("Arial", 11))
            theme_entry.insert(0, full_lesson["theme"])
            theme_entry.pack(fill="x", pady=5)
            
            # Возрастная группа
            tk.Label(edit_content, text="Возрастная группа:", font=("Arial", 11, "bold"), 
                    bg="#fffacd", fg="#2e7d32").pack(anchor="w", pady=5)
            age_groups = ["Дети 1-3 года", "Дошкольники 4-7 лет", "Школьники 8-15 лет"]
            age_var_edit = tk.StringVar(value=full_lesson["age_group"])
            age_combo_edit = ttk.Combobox(edit_content, textvariable=age_var_edit, 
                                        values=age_groups, width=50, state="readonly")
            age_combo_edit.pack(fill="x", pady=5)
            
            # Длительность
            tk.Label(edit_content, text="Длительность (мин):", font=("Arial", 11, "bold"), 
                    bg="#fffacd", fg="#2e7d32").pack(anchor="w", pady=5)
            duration_entry = tk.Entry(edit_content, width=50, font=("Arial", 11))
            duration_entry.insert(0, str(full_lesson["duration"]))
            duration_entry.pack(fill="x", pady=5)
            
            # План урока
            tk.Label(edit_content, text="План урока:", font=("Arial", 11, "bold"), 
                    bg="#fffacd", fg="#2e7d32").pack(anchor="w", pady=5)
            plan_text = scrolledtext.ScrolledText(edit_content, width=85, height=18, 
                                                  font=("Courier", 10), bg="#ffffff", fg="#333333")
            plan_text.pack(fill="x", pady=5)
            plan_text.insert("1.0", full_lesson["lesson_plan"])
            
            def save_edited_lesson():
                try:
                    new_theme = theme_entry.get().strip()
                    new_age_group = age_var_edit.get().strip()
                    new_duration = int(duration_entry.get().strip())
                    new_plan = plan_text.get("1.0", tk.END).strip()
                    
                    if not new_theme or not new_age_group or not new_duration or not new_plan:
                        messagebox.showwarning("Предупреждение", "Заполните все поля")
                        return
                    
                    new_title = f"{new_theme} ({new_age_group})"
                    
                    db_service.db_update_lesson(
                        lesson_id=lesson_id,
                        title=new_title,
                        theme=new_theme,
                        age_group=new_age_group,
                        duration=new_duration,
                        lesson_plan=new_plan
                    )
                    
                    messagebox.showinfo("Успех", "Урок успешно обновлен!")
                    edit_window.destroy()
                    lessons_win.destroy()
                    show_saved_lessons_window(root_parent)
                    
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректную длительность (число)")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось сохранить изменения: {e}")
            
            # Кнопки размещаем вне области прокрутки
            btn_frame_edit = tk.Frame(main_edit_frame, bg="#fffacd", pady=10)
            btn_frame_edit.pack(side="bottom", fill="x", padx=20, pady=10)
            
            tk.Button(btn_frame_edit, text="💾 Сохранить изменения", font=("Arial", 12, "bold"),
                     bg="#4CAF50", fg="white", width=20, height=2,
                     activebackground="#45a049", relief="flat", bd=0, cursor="hand2",
                     command=save_edited_lesson).pack(side="left", padx=10)
            
            tk.Button(btn_frame_edit, text="❌ Отмена", font=("Arial", 12, "bold"),
                     bg="#D32F2F", fg="white", width=15, height=2,
                     activebackground="#C62828", relief="flat", bd=0, cursor="hand2",
                     command=edit_window.destroy).pack(side="left", padx=10)
        
        # Функция для удаления урока
        def delete_lesson(lesson_id):
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот урок?"):
                db_service.db_delete_lesson(lesson_id)
                messagebox.showinfo("Успех", "Урок удален")
                lessons_win.destroy()
                show_saved_lessons_window(root_parent)
        
        # Отображаем каждый урок
        for i, lesson in enumerate(lessons):
            lesson_frame = tk.Frame(scrollable_frame, bg="#e8f5e9", relief="solid", bd=2, padx=15, pady=10)
            lesson_frame.pack(fill="x", pady=5, padx=10)
            
            # Информация об уроке
            info_frame = tk.Frame(lesson_frame, bg="#e8f5e9")
            info_frame.pack(side="left", fill="both", expand=True)
            
            tk.Label(info_frame, text=f"📋 {lesson['title']}", 
                    font=("Arial", 14, "bold"), bg="#e8f5e9", fg="#2e7d32").pack(anchor="w")
            tk.Label(info_frame, text=f"🎯 Тема: {lesson['theme']}", 
                    font=("Arial", 11), bg="#e8f5e9", fg="#555").pack(anchor="w")
            tk.Label(info_frame, text=f"👶 Возраст: {lesson['age_group']}", 
                    font=("Arial", 11), bg="#e8f5e9", fg="#555").pack(anchor="w")
            tk.Label(info_frame, text=f"⏱️ Длительность: {lesson['duration']} мин", 
                    font=("Arial", 11), bg="#e8f5e9", fg="#555").pack(anchor="w")
            if lesson['created_by']:
                tk.Label(info_frame, text=f"👤 Автор: {lesson['created_by']}", 
                        font=("Arial", 10), bg="#e8f5e9", fg="#777").pack(anchor="w")
            
            # Кнопки
            btn_frame = tk.Frame(lesson_frame, bg="#e8f5e9")
            btn_frame.pack(side="right")
            
            tk.Button(btn_frame, text="👁️ Просмотр", font=("Arial", 11, "bold"),
                     bg="#2196F3", fg="white", width=11, height=2,
                     activebackground="#1976D2", relief="flat", bd=0, cursor="hand2",
                     command=lambda lid=lesson['id']: view_lesson(lid)).pack(side="left", padx=3)
            
            tk.Button(btn_frame, text="✏️ Редактировать", font=("Arial", 11, "bold"),
                     bg="#FF9800", fg="white", width=12, height=2,
                     activebackground="#F57C00", relief="flat", bd=0, cursor="hand2",
                     command=lambda lid=lesson['id']: edit_lesson(lid)).pack(side="left", padx=3)
            
            tk.Button(btn_frame, text="🗑️ Удалить", font=("Arial", 11, "bold"),
                     bg="#D32F2F", fg="white", width=11, height=2,
                     activebackground="#C62828", relief="flat", bd=0, cursor="hand2",
                     command=lambda lid=lesson['id']: delete_lesson(lid)).pack(side="left", padx=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    lessons_win.mainloop()


# --- Окно игровых занятий для дошкольников ---
def show_preschool_activities_window(root_parent=None):
    # Не закрываем родительское окно, просто скрываем его
    if root_parent:
        root_parent.withdraw()  # Скрываем вместо закрытия
    
    activities_win = tk.Tk()
    activities_win.title("Игровые занятия для дошкольников")
    activities_win.geometry("750x700")
    activities_win.resizable(False, False)
    activities_win.configure(bg="#fffacd")  # Бледно-желтый фон
    
    center_window(activities_win)
    
    # Заголовок
    header_frame = tk.Frame(activities_win, bg="#4CAF50", height=100)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    # Кнопка "Назад" в левом углу
    def go_back():
        activities_win.destroy()
        if root_parent:
            root_parent.deiconify()  # Показываем родительское окно обратно
        else:
            Menu()  # Если нет родительского окна, создаем новое меню
    
    back_btn = tk.Button(header_frame, text="← Назад", font=("Arial", 10, "bold"),
                        bg="#2E7D32", fg="white", width=8, height=1,
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#1B5E20", command=go_back)
    back_btn.place(x=10, y=35)
    
    tk.Label(header_frame, text="🎨 Игровые занятия для дошкольников", 
             font=("Arial", 20, "bold"), bg="#4CAF50", fg="white").pack(pady=25)
    
    # Контейнер для занятий
    container = tk.Frame(activities_win, bg="#fffacd", padx=30, pady=20)
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
        activity_win.configure(bg="#fffacd")  # Бледно-желтый фон
        center_window(activity_win)
        
        # Заголовок занятия
        header = tk.Frame(activity_win, bg="#4CAF50", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Кнопка "Назад" в левом углу
        back_btn = tk.Button(header, text="← Назад", font=("Arial", 9, "bold"),
                            bg="#2E7D32", fg="white", width=7, height=1,
                            relief="flat", bd=0, cursor="hand2",
                            activebackground="#1B5E20", command=activity_win.destroy)
        back_btn.place(x=10, y=25)
        
        tk.Label(header, text=activity["title"], 
                font=("Arial", 18, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
        
        # Основной контент
        content = tk.Frame(activity_win, bg="#fffacd", padx=30, pady=20)
        content.pack(fill="both", expand=True)
        
        # Описание
        tk.Label(content, text="Описание занятия:", 
                font=("Arial", 12, "bold"), bg="#fffacd", fg="#2e7d32").pack(anchor="w", pady=(0, 5))
        tk.Label(content, text=activity["description"], 
                font=("Arial", 11), bg="#fffacd", fg="#555").pack(anchor="w", pady=(0, 15))
        
        # Детали
        tk.Label(content, text="Что включено:", 
                font=("Arial", 12, "bold"), bg="#fffacd", fg="#2e7d32").pack(anchor="w", pady=(0, 5))
        
        details_frame = tk.Frame(content, bg="#e8f5e9", relief="solid", bd=1, padx=15, pady=10)
        details_frame.pack(fill="x", pady=(0, 15))
        tk.Label(details_frame, text=activity["details"], 
                font=("Arial", 11), bg="#e8f5e9", fg="#333", justify="left").pack(anchor="w")
        
        # Кнопка закрыть
        tk.Button(content, text="✅ Закрыть", font=("Arial", 12, "bold"),
                  bg="#4CAF50", fg="white", width=15, height=2,
                  activebackground="#45a049", relief="flat", bd=0, cursor="hand2",
                  command=activity_win.destroy).pack(pady=20)
    
    # Создаём кнопки для каждого занятия
    for i, activity in enumerate(activities):
        btn_frame = tk.Frame(container, bg="#fffacd")
        btn_frame.pack(pady=10, fill="x")
        
        btn = tk.Button(btn_frame, text=f"{activity['title']}\n\n{activity['description']}",
                        font=("Arial", 12, "bold"), bg="#66bb6a", fg="white",
                        height=3, relief="flat", bd=0,
                        activebackground="#4caf50", cursor="hand2",
                        wraplength=650, justify="center", anchor="w")
        btn.pack(padx=10, pady=5, fill="x")
        btn.bind("<Button-1>", lambda e, a=activity: open_activity(a))
    
    # Кнопка возврата
    back_frame = tk.Frame(container, bg="#fffacd")
    back_frame.pack(pady=20)
    
    def back_to_menu():
        activities_win.destroy()
        if root_parent:
            root_parent.deiconify()  # Показываем родительское окно обратно
        else:
            Menu()  # Если нет родительского окна, создаем новое меню
    
    tk.Button(back_frame, text="🔙 Назад в главное меню", 
              font=("Arial", 11, "bold"), bg="#8BC34A", fg="white",
              width=30, height=2, relief="flat", bd=0,
              activebackground="#689F38", cursor="hand2",
              command=back_to_menu).pack()
    
    activities_win.mainloop()


# --- Окно клубов для школьников ---
def show_school_clubs_window(root_parent=None):
    # Не закрываем родительское окно, просто скрываем его
    if root_parent:
        root_parent.withdraw()  # Скрываем вместо закрытия
    
    clubs_win = tk.Tk()
    clubs_win.title("Клубы для школьников")
    clubs_win.geometry("750x700")
    clubs_win.resizable(False, False)
    clubs_win.configure(bg="#fffacd")  # Бледно-желтый фон
    
    center_window(clubs_win)
    
    # Заголовок
    header_frame = tk.Frame(clubs_win, bg="#4CAF50", height=100)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    # Кнопка "Назад" в левом углу
    def go_back():
        clubs_win.destroy()
        if root_parent:
            root_parent.deiconify()  # Показываем родительское окно обратно
        else:
            Menu()  # Если нет родительского окна, создаем новое меню
    
    back_btn = tk.Button(header_frame, text="← Назад", font=("Arial", 10, "bold"),
                        bg="#2E7D32", fg="white", width=8, height=1,
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#1B5E20", command=go_back)
    back_btn.place(x=10, y=35)
    
    tk.Label(header_frame, text="🏫 Языковые клубы для школьников", 
             font=("Arial", 20, "bold"), bg="#4CAF50", fg="white").pack(pady=25)
    
    # Контейнер для клубов
    container = tk.Frame(clubs_win, bg="#fffacd", padx=30, pady=20)
    container.pack(fill="both", expand=True)
    
    # Описание
    desc_frame = tk.Frame(container, bg="#e8f5e9", relief="solid", bd=1, padx=15, pady=10)
    desc_frame.pack(fill="x", pady=(0, 15))
    tk.Label(desc_frame, text="Выберите увлекательный клуб для развития английского языка!",
             font=("Arial", 11), bg="#e8f5e9", fg="#333").pack()
    
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
        club_win.configure(bg="#fffacd")  # Бледно-желтый фон
        center_window(club_win)
        
        # Заголовок клуба
        header = tk.Frame(club_win, bg="#4CAF50", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Кнопка "Назад" в левом углу
        back_btn = tk.Button(header, text="← Назад", font=("Arial", 9, "bold"),
                            bg="#2E7D32", fg="white", width=7, height=1,
                            relief="flat", bd=0, cursor="hand2",
                            activebackground="#1B5E20", command=club_win.destroy)
        back_btn.place(x=10, y=25)
        
        tk.Label(header, text=club["title"], 
                font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", wraplength=500).pack(pady=20)
        
        # Основной контент
        content = tk.Frame(club_win, bg="#fffacd", padx=30, pady=20)
        content.pack(fill="both", expand=True)
        
        # Описание
        tk.Label(content, text="Описание клуба:", 
                font=("Arial", 12, "bold"), bg="#fffacd", fg="#2e7d32").pack(anchor="w", pady=(0, 5))
        tk.Label(content, text=club["description"], 
                font=("Arial", 11), bg="#fffacd", fg="#555").pack(anchor="w", pady=(0, 15))
        
        # Детали
        tk.Label(content, text="Что включает:", 
                font=("Arial", 12, "bold"), bg="#fffacd", fg="#2e7d32").pack(anchor="w", pady=(0, 5))
        
        details_frame = tk.Frame(content, bg="#e8f5e9", relief="solid", bd=1, padx=15, pady=10)
        details_frame.pack(fill="x", pady=(0, 15))
        tk.Label(details_frame, text=club["details"], 
                font=("Arial", 11), bg="#e8f5e9", fg="#333", justify="left").pack(anchor="w")
        
        # Кнопка закрыть
        tk.Button(content, text="✅ Закрыть", font=("Arial", 12, "bold"),
                  bg="#4CAF50", fg="white", width=15, height=2,
                  activebackground="#45a049", relief="flat", bd=0, cursor="hand2",
                  command=club_win.destroy).pack(pady=20)
    
    # Создаём кнопки для каждого клуба
    for i, club in enumerate(clubs):
        btn_frame = tk.Frame(container, bg="#fffacd")
        btn_frame.pack(pady=10, fill="x")
        
        btn = tk.Button(btn_frame, text=f"{club['title']}\n\n{club['description']}",
                        font=("Arial", 11, "bold"), bg="#66bb6a", fg="white",
                        height=3, relief="flat", bd=0,
                        activebackground="#4caf50", cursor="hand2",
                        wraplength=650, justify="left", anchor="w")
        btn.pack(padx=10, pady=5, fill="x")
        btn.bind("<Button-1>", lambda e, c=club: open_club(c))
    
    # Кнопка возврата
    back_frame = tk.Frame(container, bg="#fffacd")
    back_frame.pack(pady=20)
    
    def back_to_menu():
        clubs_win.destroy()
        if root_parent:
            root_parent.deiconify()  # Показываем родительское окно обратно
        else:
            Menu()  # Если нет родительского окна, создаем новое меню
    
    tk.Button(back_frame, text="🔙 Назад в главное меню", 
              font=("Arial", 11, "bold"), bg="#8BC34A", fg="white",
              width=30, height=2, relief="flat", bd=0,
              activebackground="#689F38", cursor="hand2",
              command=back_to_menu).pack()
    
    clubs_win.mainloop()


# --- Функция выхода из аккаунта ---
def logout_and_exit(root_window):
    """Выход из аккаунта и возврат к окну входа"""
    global current_user
    current_user = None
    root_window.destroy()
    show_login_window()


# --- Главное меню ---
def Menu():
    root = tk.Tk()
    root.title("Полиглотики — Главное меню")
    root.geometry("800x700")
    root.resizable(False, False)
    root.configure(bg="#fffacd")  # Бледно-желтый фон

    # Центрируем окно
    center_window(root)

    # Красивый заголовок с зеленым фоном
    header_frame = tk.Frame(root, bg="#4CAF50", height=120)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    # Кнопка "Выйти из аккаунта" в правом углу (только для авторизованных пользователей)
    if current_user:
        logout_btn = tk.Button(header_frame, text="🚪 Выйти", font=("Arial", 10, "bold"),
                              bg="#D32F2F", fg="white", width=10, height=1,
                              relief="flat", bd=0, cursor="hand2",
                              activebackground="#B71C1C", command=lambda: logout_and_exit(root))
        logout_btn.place(relx=0.85, y=25)
    
    tk.Label(header_frame, text="🎓 ПОЛИГЛОТИКИ", 
             font=("Arial", 32, "bold"), bg="#4CAF50", fg="white").pack(pady=(20, 5))
    tk.Label(header_frame, text="Детский языковой центр", 
             font=("Arial", 16), bg="#4CAF50", fg="white").pack(pady=(0, 20))

    # Основной контейнер
    main_container = tk.Frame(root, bg="#fffacd", padx=30, pady=20)
    main_container.pack(fill="both", expand=True)

    # Описание
    desc_frame = tk.Frame(main_container, bg="#e8f5e9", relief="solid", bd=1, padx=20, pady=15)
    desc_frame.pack(fill="x", pady=15)
    
    tk.Label(desc_frame,
             text="Комплексное развитие: пение, танцы, рисование, творчество\n"
                  "Задания на внимание, память, логику и мышление",
             font=("Arial", 12), bg="#e8f5e9", fg="#333", wraplength=650).pack()

    # Кнопки занятий
    btn_frame = tk.Frame(main_container, bg="#fffacd")
    btn_frame.pack(pady=20)
    
    # Получаем возраст пользователя
    user_age = None
    if current_user:
        user_age = current_user.get("age")
    
    # Функция для проверки доступа к дошкольным занятиям (доступны <= 7 лет, но учителям доступны всегда)
    def check_preschool_access():
        user_role = current_user.get("role") if current_user else None
        if user_role == "учитель" or user_age is None or user_age <= 7:
            root.withdraw()  # Скрываем главное меню
            show_preschool_activities_window(root)
        else:
            year_word = "лет" if user_age > 4 else ("год" if user_age == 1 else "года")
            messagebox.showinfo("⛔ Недоступно", 
                               f"🎨 Игровые занятия для дошкольников доступны только до 7 лет включительно.\n\n"
                               f"Ваш возраст: {user_age} {year_word}.\n\n"
                               f"📚 Для вас доступны клубы для школьников!\n"
                               f"Увлекательные проекты и продвинутые занятия ждут!")
    
    # Функция для проверки доступа к клубам (доступны >= 7 лет, но учителям доступны всегда)
    def check_club_access():
        user_role = current_user.get("role") if current_user else None
        if user_role == "учитель" or user_age is None or user_age >= 7:
            root.withdraw()  # Скрываем главное меню
            show_school_clubs_window(root)
        else:
            year_word = "лет" if user_age > 4 else ("год" if user_age == 1 else "года")
            messagebox.showinfo("⛔ Недоступно", 
                               f"📚 Клубы для школьников доступны только с 7 лет.\n\n"
                               f"Ваш возраст: {user_age} {year_word}.\n\n"
                               f"🎯 Изучайте материал для дошкольников!\n"
                               f"Увлекательные игры и занятия уже доступны!")

    # Создаем кнопку дошкольных занятий - меняем стиль если недоступна (недоступна > 7, но учителям доступны всегда)
    user_role = current_user.get("role") if current_user else None
    if user_role == "учитель" or user_age is None or user_age <= 7:
        tk.Button(btn_frame, text="🎨 Игровые занятия\nдля дошкольников", 
                  font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                  width=22, height=3, relief="flat", bd=0,
                  activebackground="#45a049", cursor="hand2",
                  command=check_preschool_access).grid(row=0, column=0, padx=15)
    else:
        tk.Button(btn_frame, text="🎨 Игровые занятия\nдля дошкольников", 
                  font=("Arial", 14, "bold"), bg="#A5D6A7", fg="white", 
                  width=22, height=3, relief="flat", bd=0,
                  activebackground="#81C784", cursor="hand2",
                  command=check_preschool_access).grid(row=0, column=0, padx=15)
        
        # Добавляем метку "Недоступно"
        tk.Label(btn_frame, text="👶 До 7 лет", 
                font=("Arial", 10, "italic"), bg="#fffacd", fg="#999").grid(row=1, column=0, pady=5)

    # Создаем кнопку клубов - меняем стиль если недоступна (недоступна < 7, но учителям доступны всегда)
    if user_role == "учитель" or user_age is None or user_age >= 7:
        tk.Button(btn_frame, text="📚 Клубы\nдля школьников", 
                  font=("Arial", 14, "bold"), bg="#66BB6A", fg="white", 
                  width=22, height=3, relief="flat", bd=0,
                  activebackground="#4CAF50", cursor="hand2",
                  command=check_club_access).grid(row=0, column=1, padx=15)
    else:
        tk.Button(btn_frame, text="📚 Клубы\nдля школьников", 
                  font=("Arial", 14, "bold"), bg="#A5D6A7", fg="white", 
                  width=22, height=3, relief="flat", bd=0,
                  activebackground="#81C784", cursor="hand2",
                  command=check_club_access).grid(row=0, column=1, padx=15)
        
        # Добавляем метку "Недоступно"
        tk.Label(btn_frame, text="⏳ Доступно с 7 лет", 
                font=("Arial", 10, "italic"), bg="#fffacd", fg="#999").grid(row=1, column=1, pady=5)

    # Центральная кнопка конструктора
    center_frame = tk.Frame(main_container, bg="#fffacd")
    center_frame.pack(pady=25)

    # Показываем кнопки только для учителей
    if current_user and current_user.get("role") == "учитель":
        # Кнопка конструктора
        def open_constructor():
            root.withdraw()  # Скрываем главное меню
            Constructor(root)
        
        tk.Button(center_frame, text="🛠️ Конструктор занятий", 
                  font=("Arial", 16, "bold"), bg="#8BC34A", fg="white", 
                  width=28, height=2, relief="flat", bd=0,
                  activebackground="#689F38", cursor="hand2",
                  command=open_constructor).pack(pady=5)
        
        # Кнопка сохраненных уроков
        def open_saved_lessons():
            root.withdraw()
            show_saved_lessons_window(root)
        
        tk.Button(center_frame, text="📚 Сохраненные уроки", 
                  font=("Arial", 16, "bold"), bg="#FF9800", fg="white", 
                  width=28, height=2, relief="flat", bd=0,
                  activebackground="#F57C00", cursor="hand2",
                  command=open_saved_lessons).pack(pady=5)

    # Методика
    method_frame = tk.Frame(main_container, bg="#e8f5e9", relief="solid", bd=1, padx=20, pady=12)
    method_frame.pack(fill="x", pady=10)
    
    tk.Label(method_frame,
             text="📖 Методика: One Person - One Language\n💡 Развиваем речь, восприятие, чтение, письмо",
             font=("Arial", 11), bg="#e8f5e9", fg="#555555").pack()

    # Информация о пользователе внизу
    user_frame = tk.Frame(root, bg="#C8E6C9", height=50)
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
             font=("Arial", 11), bg="#C8E6C9", fg="#555").pack(pady=12)

    root.mainloop()


# --- Окно регистрации ---
def show_register_window(login_win, login_parent_entry=None):
    reg_win = tk.Toplevel()
    reg_win.title("Регистрация")
    reg_win.geometry("450x620")
    reg_win.resizable(False, False)
    
    # Бледно-желтый фон
    reg_win.configure(bg="#fffacd")

    # Центрируем окно
    center_window(reg_win)

    # Заголовок с зеленым фоном
    header_frame = tk.Frame(reg_win, bg="#4CAF50", height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="✏️ Создайте аккаунт", 
             font=("Arial", 22, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
    
    # Создаем контейнер для полей
    container = tk.Frame(reg_win, bg="#fffacd", padx=30, pady=20)
    container.pack(fill="both", expand=True)

    # Логин с иконкой
    login_frame = tk.Frame(container, bg="#fffacd")
    login_frame.pack(fill="x", pady=10)
    tk.Label(login_frame, text="👤 Логин:", font=("Arial", 11, "bold"), 
             bg="#fffacd", fg="#2e7d32").pack(anchor="w")
    login_entry = tk.Entry(login_frame, width=35, font=("Arial", 11), 
                          highlightthickness=2, relief="solid", bd=1)
    login_entry.config(highlightbackground="#ccc", highlightcolor="#4CAF50")
    login_entry.pack(pady=5)
    
    # Пароль с иконкой
    password_frame = tk.Frame(container, bg="#fffacd")
    password_frame.pack(fill="x", pady=10)
    tk.Label(password_frame, text="🔒 Пароль:", font=("Arial", 11, "bold"), 
             bg="#fffacd", fg="#2e7d32").pack(anchor="w")
    password_entry = tk.Entry(password_frame, show="*", width=35, font=("Arial", 11),
                             highlightthickness=2, relief="solid", bd=1)
    password_entry.config(highlightbackground="#ccc", highlightcolor="#4CAF50")
    password_entry.pack(pady=5)

    # Возраст с иконкой
    age_frame = tk.Frame(container, bg="#fffacd")
    age_frame.pack(fill="x", pady=10)
    tk.Label(age_frame, text="🎂 Возраст:", font=("Arial", 11, "bold"), 
             bg="#fffacd", fg="#2e7d32").pack(anchor="w")
    age_entry = tk.Entry(age_frame, width=35, font=("Arial", 11),
                        highlightthickness=2, relief="solid", bd=1)
    age_entry.config(highlightbackground="#ccc", highlightcolor="#4CAF50")
    age_entry.pack(pady=5)

    # Роль с красивым дизайном
    role_frame = tk.Frame(container, bg="#fffacd")
    role_frame.pack(fill="x", pady=15)
    tk.Label(role_frame, text="👥 Выберите роль:", font=("Arial", 11, "bold"), 
             bg="#fffacd", fg="#2e7d32").pack(anchor="w", pady=(0, 8))
    
    role_var = tk.StringVar(value=None)

    # Стильные радиокнопки
    role_container = tk.Frame(role_frame, bg="#e8f5e9", relief="solid", bd=1)
    role_container.pack(fill="x", pady=5)
    
    tk.Radiobutton(role_container, text="🎓 Ученик", variable=role_var, value="ученик", 
                   bg="#e8f5e9", font=("Arial", 11), padx=20, pady=8,
                   selectcolor="#bbdefb", activebackground="#90caf9").pack(side="left", padx=10)
    
    tk.Radiobutton(role_container, text="👨‍🏫 Учитель", variable=role_var, value="учитель", 
                   bg="#e8f5e9", font=("Arial", 11), padx=20, pady=8,
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
    win.configure(bg="#fffacd")  # Бледно-желтый фон

    # Центрируем окно
    center_window(win)
    
    # Красивый заголовок
    header_frame = tk.Frame(win, bg="#4CAF50", height=100)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="🎓 Добро пожаловать!", 
             font=("Arial", 26, "bold"), bg="#4CAF50", fg="white").pack(pady=25)
    
    # Контейнер для полей
    container = tk.Frame(win, bg="#fffacd", padx=40, pady=30)
    container.pack(fill="both", expand=True)

    # Логин
    login_frame = tk.Frame(container, bg="#fffacd")
    login_frame.pack(fill="x", pady=15)
    tk.Label(login_frame, text="👤 Логин:", font=("Arial", 11, "bold"), 
             bg="#fffacd", fg="#2e7d32").pack(anchor="w")
    login_entry = tk.Entry(login_frame, width=35, font=("Arial", 11),
                          highlightthickness=2, relief="solid", bd=1)
    login_entry.config(highlightbackground="#ccc", highlightcolor="#4CAF50")
    login_entry.pack(pady=5)

    # Пароль
    password_frame = tk.Frame(container, bg="#fffacd")
    password_frame.pack(fill="x", pady=15)
    tk.Label(password_frame, text="🔒 Пароль:", font=("Arial", 11, "bold"), 
             bg="#fffacd", fg="#2e7d32").pack(anchor="w")
    password_entry = tk.Entry(password_frame, show="*", width=35, font=("Arial", 11),
                             highlightthickness=2, relief="solid", bd=1)
    password_entry.config(highlightbackground="#ccc", highlightcolor="#4CAF50")
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
              bg="#4CAF50", fg="white", width=20, height=2,
              activebackground="#45a049", activeforeground="white",
              relief="flat", bd=0, cursor="hand2",
              command=login).pack(pady=(0, 10))

    # Кнопка регистрации
    tk.Button(container, text="✨ Создать аккаунт", font=("Arial", 12, "bold"), 
              bg="#8BC34A", fg="white", width=20, height=2,
              activebackground="#689F38", activeforeground="white",
              relief="flat", bd=0, cursor="hand2",
              command=lambda: show_register_window(win, login_entry)).pack(pady=10)
    
    # Текст под кнопками
    tk.Label(container, text="Нет аккаунта? Нажмите кнопку выше", 
             font=("Arial", 10), bg="#fffacd", fg="#999").pack(pady=5)
    
    # Фокус на первое поле
    login_entry.focus()

    win.mainloop()

