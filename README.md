# Сервис покупки товаров для авторизованных пользователей

## Описание проекта

Данный проект представляет собой API backend для сервиса покупки товаров для 
авторизованных пользователей, разработанный на основе следующего стека технологий:
Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL. Сервис предоставляет возможность 
пользователям регистрироваться, авторизоваться, 
просматривать доступные товары, а также управлять своей корзиной.

## Основные функциональные возможности

- Регистрация пользователей: Пользователи могут создать учетную запись, предоставляя свои ФИО, email, телефон и пароль.
- Авторизация пользователей: Пользователи могут авторизоваться с использованием email или телефона и пароля.
- Работа с товарами: Администраторы могут добавлять, редактировать и удалять товары, а все пользователи могут только просматривать доступные товары.
- Корзина: Пользователи могут добавлять товары в корзину, удалять их и получать общую стоимость товаров в корзине.

## Структура проекта


<br>.
<br>├── migration/             # Директория с миграциями alembic
<br>├── src/                   # Директория с приложениями
<br>│   ├── product_service/   # Приложение продаж со своими моделями, роутерами и схемами
<br>│   ├── users/             # Приложение аутентификации пользователей со своими моделями, роутерами и схемами
<br>│   ├── config.py          # Основной конфигурационный файл проекта
<br>│   ├── crud.py            # Основной CRUD-класс(родительский)
<br>│   ├── database.py        # Подключение к базе данных
<br>│   ├── exceptions.py      # Созданные исключения
<br>│   ├── main.py            # Файл запуска проекта
<br>│   └── models.py          # Базовая модель(родительская)
<br>├── tests/                 # Тесты
<br>│   ├── conftest.py        # Фикстуры и преднастройка тестов
<br>│   ├── fixture.json       # Данные для наполнения тестовой базы данных
<br>│   ├── utils.py           # Функция наполняющая базу данных
<br>│   └── test_main.py       # Основные тесты проекта
<br>├── .env                   # Хранилище переменных окружения
<br>├── .gitignore             # Храналище имен игнорируемых системой контроля версий
<br>├── docker-compose.yml     # Составной докер
<br>├── Dockerfile             # Докер-файл для запуска python
<br>├── env.sample             # Пример заполнения .env
<br>├── pytest.ini             # Настройки для тестирования
<br>├── alembic.ini            # Настройки alembic
<br>├── README.md              # Описание проекта
<br>└── requirements.txt       # Библиотеки и их версии, необходимые для запуска проекта


## Установка и запуск

### Предварительные требования

- Установленный [Docker](https://www.docker.com/get-started)
- Установленный [Docker Compose](https://docs.docker.com/compose/install/)
- Необходимые права доступа для создания Docker контейнеров

### Установка

1. Клонируйте репозиторий:

   git clone https://github.com/InsatiateDevil/Product_sale_service
   
   Перейдите в папку проекта
   Произведите настройку виртуального окружения, заполнив .env файл по примеру env.sample

2. Соберите Docker образ и запустите контейнеры:

   docker-compose up --build

   для запуска в фоном режиме можно использовать следующую комманду:

   docker-compose up --build -d


### Запуск

После успешной сборки и запуска контейнеров, приложение будет доступно по адресу http://localhost:8000.

### Документация API

Swagger UI будет доступен по следующему адресу: [http://localhost:8000/docs](http://localhost:8000/docs).

