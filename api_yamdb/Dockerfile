FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY / /app

WORKDIR /app

RUN python3 manage.py makemigrations users
RUN python3 manage.py makemigrations reviews
RUN python3 manage.py spectacular --color --file schema.yml

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
