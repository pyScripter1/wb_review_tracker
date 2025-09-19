# wb_review_tracker
Сервис для отслеживания отзывов на wb

## Возможности
* Автоматический сбор отзывов с Wildberries API
* Фильтрация отзывов по рейтингу (плохие отзывы)
* Сохранение в базу данных с защитой от дубликатов
* Гибкая настройка периода сбора отзывов
* Подробное логирование всех операций
* Асинхронная реализация для высокой производительности

## Технологический стек
* Python 3.9+
* SQLAlchemy - ORM для работы с БД
* HTTpx - асинхронные HTTP-запросы
* Loguru - продвинутое логирование
* SQLite

## Установка

Клонируйте репозиторий
```bash
git clone https://github.com/pyScripter1/wb_review_tracker.git
cd wb_review_tracker
```

Установите зависимости
```bash
pip install -r requirements.txt
```

## Использование

Базовое использование
```bash
python main.py 12345678
```
Где 12345678 - артикул товара на Wildberries

Использование с расширенными параметрами
```bash
# С отзывами с рейтингом ниже 4 за последние 7 дней
python main.py 12345678 --min-rating 4 --days-back 7

# Только очень плохие отзывы (1-2 звезды)
python main.py 12345678 --min-rating 3
```

## Структура проекта
```text
wb_review_tracker/
├── models.py          # Модели данных SQLAlchemy
├── database.py        # Управление подключением к БД
├── wb_api.py          # Клиент API Wildberries
├── service.py         # Бизнес-логика сервиса
├── main.py           # Точка входа, CLI интерфейс
├── config.py         # Конфигурация приложения
└── requirements.txt  # Зависимости проекта
```

## Пример работы
```log
2024-01-15 10:30:45 | INFO | Starting review collection for nm_id 12345678
2024-01-15 10:30:45 | INFO | Parameters: min_rating=3, days_back=3
2024-01-15 10:30:47 | INFO | Found 15 bad reviews out of 87 total
2024-01-15 10:30:48 | INFO | Saved review abc123 for product 12345678
2024-01-15 10:30:48 | INFO | Successfully saved 15 bad reviews
```

