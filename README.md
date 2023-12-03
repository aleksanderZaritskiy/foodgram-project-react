# Foodgram - Учебный проект Яндекс.Практикум

![Github Actions main workflow](https://github.com/apicqq/foodgram-project-react/actions/workflows/main.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Использованные при реализации проекта технологии
 - Python
 - Django
 - djangorestframework
 - Nginx
 - gunicorn
 - PostgreSQL
 - Docker

## Установка проекта на локальный компьютер из репозитория 

### Для установки проекта необходимо выполнить следующие шаги:

### Базовая настройка:
 - Клонировать репозиторий `git clone <адрес вашего репозитория>`
 - Перейти в директорию с клонированным репозиторием
 - Cоздать файл `.env` и заполнить его переменными по примеру из файла 

---
### Настройка Nginx:
Устанавливаем nginx:
- `sudo apt install nginx -y`

И сразу запускаем его:
- `sudo systemctl start nginx`

Включаем файервол:
- `sudo ufw enable`

Открываем конфигурационный файл nginx по адресу: `/etc/nginx/sites-enabled/default` и редактируем его:
```text
server {
    server_name IP_адрес_сервера домен_сервера;
    server_tokens off;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```
Сохраняем изменения, выходим из редактора и проверяем корректность настроек:
- `sudo nginx -t`

Перезапускаем nginx для применения изменений:
- `sudo systemctl reload nginx`
---


### Настройка и установка Docker:
Находясь на сервере, последовательно выполните команды:
   - `sudo apt update`
   - `sudo apt install curl`
   - `curl -fSL https://get.docker.com -o get-docker.sh`
   - `sudo sh ./get-docker.sh`
   - `sudo apt-get install docker-compose-plugin`

Далее, выполните следующие команды для запуска проекта на локальной машине:
 - `sudo docker compose -f docker-compose.production.yml pull`
 - `sudo docker compose -f docker-compose.production.yml down`
 - `sudo docker compose -f docker-compose.production.yml up -d`
 - `sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate`
 - `sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic`
 - `sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/`

Проект будет доступен по адресу: `http://localhost:8000/`

---

Демо-версия проекта доступна по адресу: `https://deployfoodgram.sytes.net/`

Данные для входа в админ-зону:
    почта: admin@mail.ru,
    пароль: admin
    
## Автор проекта

[Зарицкий Александр](https://github.com/aleksanderZaritskiy)


