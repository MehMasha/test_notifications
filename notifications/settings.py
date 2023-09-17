import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = 'django-insecure-vmj68do!=^fp5-1vcya*eh25^s&2yaxljzrm(@=zsq$fpiu4h_'

DEBUG = True

ALLOWED_HOSTS = ["192.168.0.14", "localhost", '127.0.0.1', '95.163.230.19']


ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', '')
SERVICE_URL = os.getenv('SERVICE_URL', '')

SERVICE_HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.mailing',
    'apps.clients',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'notifications.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'notifications.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv('POSTGRES_DB', 'postgres'),
#         "USER": os.getenv('POSTGRES_USER', 'postgres'),
#         "PASSWORD": os.getenv('POSTGRES_PASSWORD', 'postgres'),
#         "HOST": os.getenv('POSTGRES_HOST', ''),
#         "PORT": os.getenv('POSTGRES_PORT', 5432),
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": 'postgres',
#         "USER": 'postgres',
#         "PASSWORD": 'postgres',
#         "HOST": 'db',
#         "PORT": 5432,
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

CELERY_BEAT_SCHEDULE = {
    'check-mailing-time': {
        'task': 'api.tasks.check_mailings',
        'schedule': crontab(minute='*/1'),
    },
}


# SPECTACULAR_SETTINGS = {
#     'TITLE': 'Notification API',
#     'DESCRIPTION': 'Description',
#     'VERSION': '1.0.0',
#     'SERVE_INCLUDE_SCHEMA': False,
# }

REST_FRAMEWORK = {}
