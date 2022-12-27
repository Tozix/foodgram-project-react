## Проект Foodgram
![workflow](https://github.com/Tozix/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)
___
### Описание
Foodgram - это продуктовый помощник с рецептами. Он позволяет публиковать рецепты, сохранять избранное и создавать список покупок для выбранных рецептов. Вы можете подписаться на любимых авторов.

- Проект доступен по [адресу](https://foodgram.boostnet.ru)
- Документация к API доступна [здесь](https://foodgram.boostnet.ru/api/docs/)
___
### Технологии
- [Python]
- [Django]
- [Django REST Framework]
- [Django import / export]
- [Docker]
- [Gunicorn]
- [PostgreSQL]
___

## Шаблон наполнения .env
```
# секретный ключ Django проекта
SECRET_KEY='asdasdasdsW45RF324ADSTAST4ADFS'     
# Дебаг режим
DEBUG=True
# Список разршенных хостов через запятую
ALLOWED_HOSTS='*,localhost' 
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
DB_HOST='db'
# 5432 (порт по умолчанию)
DB_PORT=5432                 

```

## Автоматизация развертывания серверного ПО
Для автоматизации развертывания ПО на боевых серверах используется среда виртуализации Docker, а также Docker-compose - инструмент для запуска многоконтейнерных приложений. Docker позволяет «упаковать» приложение со всем его окружением и зависимостями в контейнер, который может быть перенесён на любую Linux -систему, а также предоставляет среду по управлению контейнерами. Таким образом, для разворачивания серверного ПО достаточно чтобы на сервере с ОС семейства Linux были установлены среда Docker и инструмент Docker-compose.

Ниже представлен docker-compose.yaml - файл с инструкцией по разворачиванию Docker-контейнера приложения:

```Dockerfile
version: '3.8'

services:

  db:
    image: postgres:13.0-alpine
    volumes:
      - data_value:/var/lib/postgresql/data/
    env_file:
      - ./.env
    restart: always

  backend:
    image: tozix/foodgram-back:latest
    restart: always
    volumes:
      - static_value:/app/static/
      - media_value:/app/media/
      - redoc:/app/api/docs/
    env_file:
      - ./.env
    depends_on:
      - db

  frontend:
    image: tozix/foodgram-front:latest
    volumes:
      - ../frontend/:/app/result_build/
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./certbot/www:/var/www/certbot/:ro
      - ./certbot/conf/:/etc/nginx/ssl/:ro
      - ../frontend/build:/usr/share/nginx/html/
      - static_value:/var/html/static/
      - media_value:/var/html/media/
      - redoc:/usr/share/nginx/html/api/docs/
    depends_on:
      - backend
    restart: always

  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/www/:/var/www/certbot/:rw
      - ./certbot/conf/:/etc/letsencrypt/:rw
    depends_on:
      - nginx

volumes:
  static_value:
  media_value:
  data_value:
  redoc:
```



## Описание команд для запуска приложения в контейнерах
Для запуска проекта в контейнерах используем **docker-compose** : ```docker-compose up -d --build```, находясь в директории (infra) с ```docker-compose.yaml```

После сборки контейнеров выполяем:
```bash
# Выполняем миграции
docker-compose exec backend python manage.py migrate
# Создаем суперппользователя
docker-compose exec backend python manage.py createsuperuser
# Собираем статику со всего проекта
docker-compose exec backend python manage.py collectstatic --no-input
```
Пример настройки хоста для nginx
```
server {
    listen 80;
    listen [::]:80;
    server_name foodgram.boostnet.ru;
    server_tokens off;
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    if ($host = foodgram.boostnet.ru) {
        return 301 https://$host$request_uri;
    }
}

server {
    server_tokens off;
    listen 443 default_server ssl http2;
    listen [::]:443 ssl http2;
    server_name foodgram.boostnet.ru;
    ssl_certificate /etc/nginx/ssl/live/foodgram.boostnet.ru/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/foodgram.boostnet.ru/privkey.pem;

    location /media/ {
        root /var/html;
    }

    location /static/admin {
        root /var/html;
    }

    location /static/rest_framework/ {
        root /var/html/;
    }

    location /admin/ {
        proxy_pass http://backend:8000/admin/;
    }

    location /api/docs/ {
        root /usr/share/nginx/html;
        try_files $uri $uri/redoc.html;
    }

    location /api/ {
        proxy_set_header Host $host;
        proxy_set_header        X-Forwarded-Host $host;
        proxy_set_header        X-Forwarded-Server $host;
        proxy_pass http://backend:8000;
    }

    location / {
        root /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri /index.html;
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;
    }
    
    error_page   500 502 503 504  /50x.html;

    location = /50x.html {
        root   /var/html/frontend/;
    }

}

```
## Админ для Ревью
- email: admin@test.net
- Password: RfdS2sf5yhga


## Импорт/Экспорт данных
Импорт/либо экспорт данных можно произвести через админ панель сайта по [адресу](https://foodgram.boostnet.ru/admin/)

### Автор backend'а:
[Никита Емельянов]


[//]: # (Ниже находятся справочные ссылки)

   [Python]: <https://www.python.org/downloads/release/python-370/>
   [Django]: <https://www.djangoproject.com/download/>
   [Django REST Framework]: <https://www.django-rest-framework.org/community/release-notes/>
   [Django import / export]: <https://django-import-export.readthedocs.io/en/latest/>
   [Docker]: <https://www.docker.com/>
   [Gunicorn]: <https://gunicorn.org/>
   [PostgreSQL]:<https://www.postgresql.org/>  
   [Никита Емельянов]: <https://github.com/Tozix>

