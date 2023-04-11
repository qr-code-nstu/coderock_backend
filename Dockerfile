# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.11-alpine

WORKDIR /app
RUN mkdir -p $WORKDIR/static
RUN mkdir -p $WORKDIR/media
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Устанавливает рабочий каталог контейнера — "app"
RUN pip install --upgrade pip
# Копирует все файлы из нашего локального проекта в контейнер
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .