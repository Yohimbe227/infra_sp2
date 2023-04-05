
# Учебный проект api_yambd
### Содержание и возможности:
Проект YaMDb собирает отзывы пользователей на произведения. 
* Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. 
* Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
* Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
* Добавлять произведения, категории и жанры может только администратор. 
* Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку.
## Authors

Никулин Илья | Каманин Юрий   | Решетняк Михаил 
-----------|:------------------------------------------------:| :----------|
[@1darkhorse1](https://www.github.com/1darkhorse1) | [@Yohimbe227](https://www.github.com/Yohimbe227) | [@Jelister203](https://www.github.com/Jelister203)

## Installation

Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/1darkhorse1/api_yamdb.git
```
```bash
cd api_yamdb/
```
Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python manage.py migrate
```
Запустить проект:
```bash
python manage.py runserver
```

## API Enpoints

```http
GET, POST /api/v1/users/
GET, PATCH, DELETE /api/v1/users/{username}/
GET, PATCH /api/v1/users/me/
```

```http
GET, POST /api/v1/titles/
GET, PATCH, DELETE /api/v1/titles/{title_id}/
```
```http
GET, POST /api/v1/categories/
DEL /api/v1/categories/{slug}/
```
```http
GET, POST /api/v1/genres/
DELETE /api/v1/genres/{slug}/
```
```http
GET, POST /api/v1/titles/{title_id}/reviews/
GET, PATCH, DELELE /api/v1/titles/{title_id}/reviews/{review_id}/
```
```http
GET, POST/api/v1/titles/{title_id}/reviews/{review_id}/comments/
GET, PATCH, DELELE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
### Without token authentication, limited functionality
Urls by which you can send GET requests to API: 
* "categories": /api/v1/categories/, 
* "genres": "/api/v1/genres/", 
* "titles": "/api/v1/titles/", 
* "reviews": "/api/v1/titles/{title_id}/reviews/", 
* "comments": "/api/v1/titles/{title_id}/reviews/{review_id}/comments/" 
* "users": "/api/v1/users/"

### Authentication
* POST requests /api/v1/auth/signup/: {"username": "user", "email": "example@example.ru"}
* copy the confirmation code in the sent_emails folder
* POST request /api/v1/auth/token/: {"username": "user111", "confirmation_code": ""}

## Filling the database from a csv file
The files must be located in the /static/data/ directory.
Valid names and headers:

Файл    | Заголовок 
-----------|:-------: 
category.csv       |   name, slug 
genre.csv    |   name, slug
users.csv      | username, email, role, bio, first_name, last_name
titles.csv      | name,year,category
review.csv      |   itle_id, text, author, score, pub_date  
genre_title.csv  | title_id, genre_id
comments.csv    | review_id, text, author, pub_date

The filling of the base is performed by Django managment command:
```bash
python manage.py csv_to_base
```
Duplicate table rows will be ignored.