# Проект api_yambd
_**Основной стэк**_:  
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

**Проект был выполнен в учебных целях, чтобы попрактиковаться в командной
работе с библиотеками Django, Django REST fraemwork и технологией Docker.**
## Содержание и возможности

Проект YaMDb собирает отзывы пользователей на произведения.

* Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или
послушать музыку.
* Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
* Произведению может быть присвоен жанр из списка предустановленных (например,
«Сказка», «Рок» или «Артхаус»).
* Добавлять произведения, категории и жанры может только администратор.
* Благодарные или возмущённые пользователи оставляют к произведениям текстовые
отзывы и ставят произведению оценку.

## Authors

| Никулин Илья                                       |                   Каманин Юрий                   | Решетняк Михаил                                    |
|----------------------------------------------------|:------------------------------------------------:|:---------------------------------------------------|
| [@1darkhorse1](https://www.github.com/1darkhorse1) | [@Yohimbe227](https://www.github.com/Yohimbe227) | [@Jelister203](https://www.github.com/Jelister203) |

## Installation

Создайте в директории infra файл .env по шаблону:

```bash
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=your_password # пароль для подключения к БД (установите свой)
    DB_HOST=db
    DB_PORT=5432
```

Для запуска приложения необходимо:  
выполнить миграции:

```bash
python manage.py migrate
```

создать суперпользователя:

```bash
python manage.py createsuperuser
```

собрать статику:

```bash
python manage.py collectstatic --no-input
```

## API Enpoints

<http://127.0.0.1/api/schema/redoc>

### Authentication

* POST requests /api/v1/auth/signup/:
{"username": "user", "email": "example@example.ru"}
* copy the confirmation code in the sent_emails folder
* POST request /api/v1/auth/token/:
{"username": "user111", "confirmation_code": ""}

## Filling the database from a csv file

The files must be located in the /static/data/ directory.
Valid names and headers:

| Файл            |                     Заголовок                     |
|-----------------|:-------------------------------------------------:|
| category.csv    |                    name, slug                     |
| genre.csv       |                    name, slug                     |
| users.csv       | username, email, role, bio, first_name, last_name |
| titles.csv      |                name,year,category                 |
| review.csv      |      itle_id, text, author, score, pub_date       |
| genre_title.csv |                title_id, genre_id                 |
| comments.csv    |         review_id, text, author, pub_date         |

The filling of the base is performed by Django managment command:

```bash
python manage.py csv_to_base
```

Duplicate table rows will be ignored.
