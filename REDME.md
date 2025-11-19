# Проект тестирования сайта "Читай Город"

Проект автоматизированного тестирования веб-сайта "Читай Город" с поддержкой UI и API тестов.


     Задача проекта

Автоматизировать тестирование ключевых функций интернет-магазина:

Поиск товаров (кириллица, латиница, цифры, спецсимволы)

Работа с корзиной (добавление/удаление товаров)

Навигация по каталогу

API тестирование (доступность, поисковые запросы)



     Структура проекта

DIPLOM/
├── config/                 # Конфигурационные файлы
│   ├── settings.py        # Настройки проекта
│   └── test_data.py       # Тестовые данные
├── pages/                 # Page Object Model
│   ├── base_page.py       # Базовый класс страниц
│   ├── main_page.py       # Главная страница
│   ├── search_page.py     # Страница поиска
│   └── cart_page.py       # Страница корзины
├── test/                  # Тестовые сценарии
│   ├── test_ui.py         # UI тесты
│   └── test_api.py        # API тесты
├── utils/                 # Вспомогательные утилиты
│   ├── driver_factory.py  # Фабрика WebDriver
│   └── helpers.py         # API хелперы
└── Документация
    ├── README.md          # Этот файл
    ├── pytest.ini         # Конфигурация pytest
    ├── requirements.txt   # Зависимости Python
    └── .gitignore         # Исключения Git

### Игнорируемые файлы

Проект включает файл `.gitignore` который исключает из контроля версий:

- Файлы Python кэша (`__pycache__/`, `*.pyc`)
- Виртуальные окружения (`venv/`, `.venv/`)
- Файлы IDE (`.vscode/`, `.idea/`)
- Логи и отчеты тестов
- Скриншоты и временные файлы
- Драйверы браузеров
- Allure отчеты
- Конфигурационные файлы с чувствительными данными

### Важные исключения

**Не игнорируются**:
- `config/settings.py` - настройки по умолчанию
- `config/test_data.py` - тестовые данные
- `requirements.txt` - зависимости проекта

### Для разработки

1. Не коммитьте чувствительные данные (пароли, токены)
2. Используйте `config/local/` для локальных настроек
3. Добавляйте в `.gitignore` файлы специфичные для вашей среды

    Установка зависимостей

# Клонирование репозитория
git clone <repository-url>
cd chitai-gorod-tests

# Установка зависимостей
pip install -r requirements.txt


     Настройка окружения

Проверьте настройки в config/settings.py:

# Основные настройки
BASE_URL = "https://www.chitai-gorod.ru"
BROWSER = "chrome"
HEADLESS = False  # Измените на True для безголового режима

     Запуск тестов
Базовые команды:

# Запуск всех тестов
pytest

# Запуск только UI тестов
pytest --ui

# Запуск только API тестов  
pytest --api

# Запуск с детальным выводом
pytest -v

# Запуск с HTML отчетом
pytest --html=report.html
Запуск с Allure отчетами:

# Запуск тестов с сохранением результатов Allure
pytest --alluredir=allure-results

# Генерация и открытие отчета
allure serve allure-results

# Или генерация статического отчета
allure generate allure-results -o allure-report

     Тестовые сценарии

    UI Тесты (test_ui.py)
test_search_latin - Поиск книги на латинице ("harry potter")

test_search_numeric - Поиск названия из цифр ("1984")

test_search_special_chars - Поиск с спецсимволами ("C#")

test_search_by_catalog - Навигация по каталогу товаров

test_search_and_add_to_cart - Поиск и добавление товара в корзину


    API Тесты (test_api.py)
test_site_availability - Проверка доступности сайта

test_search_cyrillic - Поиск по кириллице через API

test_search_cyrillic_with_numbers - Поиск с цифрами через API

test_empty_search - Тест пустого поиска

test_search_without_token - Поиск без авторизации

test_search_wrong_method - Поиск с неправильным HTTP методом

    Конфигурация
Настройки в config/settings.py

# URL и API
BASE_URL = "https://www.chitai-gorod.ru"
API_SEARCH_URL = "https://www.chitai-gorod.ru/search"

# Таймауты
IMPLICIT_WAIT = 5
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30

# Браузер
BROWSER = "chrome"
HEADLESS = False
WINDOW_SIZE = "1920x1080"


    Тестовые данные в config/test_data.py

SEARCH_DATA = {
    "latin_search": "harry potter",
    "numeric_search": "1984", 
    "cyrillic_search": "гарри поттер",
    "empty_search": "",
    "catalog_search": "алмазная мозаика"
}
     Технологии
Python 3.8+ - основной язык программирования

Selenium 4.15.0 - автоматизация браузера

Pytest 7.4.3 - фреймворк для тестирования

Allure - система отчетов

Requests - HTTP запросы для API тестов

WebDriver Manager - автоматическое управление драйверами

     Генерация отчетов
Allure отчеты:

# Установка Allure
pip install allure-pytest

# Запуск тестов с генерацией отчетов
pytest --alluredir=allure-results

# Просмотр отчета
allure serve allure-results

### Предварительные требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)
- Git

  Ссылка на финальный проект:

  https://ucheba1-.yonote.ru/doc/finalnyj-proekt-SWr3nMHm0r

