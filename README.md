# test_notifications


## Используемые технологии

* Python 3.10
* Django 4.2
* DRF
* drf-yasg
* redis
* celery
* pytest
* docker
* docker compose
* prometheus
* nginx


## Запуск проекта

### Склонируйте репозиторий 

```
    git clone git@gitlab.com:MehMasha/test_notifications.git
```

### Заполните .env_fill файл и измените его название на .env
    
```
    ACCESS_TOKEN = Токен для сервиса, который занимается отправкой сообщений
    SERVICE_URL = URL сервиса, который занимается отправкой сообщений
    POSTGRES_USER = Пользователь базы данных
    POSTGRES_DB = Название базы данных
    POSTGRES_PASSWORD = Пароль пользователя базы данных
    POSTGRES_HOST = Хост базы данных(db если запускаете через docker compose)
    POSTGRES_PORT = Порт базы данных
    DEBUG = Режим отладки Django
    ALLOWED_HOSTS = allowed_hosts для настроек Djnago
    SECRET_KEY = секретный ключ Django
```

### Запустите проект командой
 
```
    docker compose up -d
```

### Создайте суперюзера для работы с админ панелью
 
```
    docker compose exec web python manage.py createsuperuser
```

## Помимо основного задания были выполнены:

* Дополнительное задание №1: Тестирование написанного кода с помощью pytest(Работает в режиме разработки)
    
* Дополнительное задание №3: Docker compose для запуска всех сервисов проекта одной командой (redis, celery, postgres, django, nginx, prometheus)

* Дополнительное задание №5: По адресу /docs/ открывается страница со Swagger UI и схожей документацией

* Дополнительное задание №6: Реализован администраторский Web UI с помощью django admin, попасть можно по /admin

* Дополнительное задание №9: Откладывание запросов при неуспехе для последующей повторной отправки

* Дополнительное задание №12: Подробное логирование на всех этапах обработки запросов в /logs/log.json


