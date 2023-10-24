import os
import environ
from pathlib import Path
from datetime import timedelta

# Set environment configuration
env = environ.Env(
    DEBUG=(bool, False),
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = env("SECRET_KEY")
SECRET_KEY_FOR_REFRESH_TOKEN = env("SECRET_KEY_FOR_REFRESH_TOKEN")

LOGGER_ROOT_NAME = env.str("LOGGER_ROOT_NAME", "Dish_Decision")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third party apps
THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'cid.apps.CidAppConfig',
]

# Project apps
# Add project apps after create new apps with django-admin startapp app_name
PROJECT_APPS = [

]
# Project installed applications
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS


# CORS CONFIG #
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
    'PATCH',
)

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'contenttype',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
# CORS CONFIG END #

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cid.middleware.CidMiddleware',
]

# DRF Conf start
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'applibs',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        "rest_framework.permissions.IsAuthenticated",
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}
# DRF conf end

ROOT_URLCONF = 'DishDecision.urls'

# django-correlation-id config
CID_GENERATE = True
CID_HEADER = 'HTTP_X_REQUEST_ID'
CID_RESPONSE_HEADER = 'X-Request-ID'
# django-correlation-id config end

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'DishDecision.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_DB_NAME'),
        'USER': env.str('POSTGRES_DB_USER'),
        'PASSWORD': env.str('POSTGRES_DB_PASSWORD'),
        'HOST': env.str('POSTGRES_DB_HOST'),
        'PORT': env.str('POSTGRES_DB_PORT'),
        'OPTIONS': env.dict('POSTGRES_DB_OPTIONS'),
        'TEST': {
            'NAME': env.str('POSTGRES_DB_TEST_NAME'),
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env.str('CACHE_NODE'),
        "KEY_PREFIX": "DISH_DECISION_",
        "TIMEOUT": env.int('CACHE_TTL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            "PASSWORD": env.str('CACHE_PASS'),
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
DEFAULT_CURRENCY = 'BDT'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/dish-decision/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# LOG Environment file
DJANGO_LOG_LEVEL = env.str('DJANGO_LOG_LEVEL', 'DEBUG')
LOG_LEVEL = env.str('LOG_LEVEL', 'DEBUG')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGGING SETUP START#
GENERAL_LOGGER = env.str('LOGGING_CHANNEL', 'general')

# Simple JWT settings starts
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=env.int("ACCESS_TOKEN_LIFETIME", 2592000)),
    "REFRESH_TOKEN_LIFETIME": timedelta(seconds=env.int("REFRESH_TOKEN_LIFETIME", 5184000)),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": "UPAY",
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(seconds=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(seconds=60),
}
# Simple JWT settings ends

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[cid: {cid}] | {asctime} | {levelname} | {pathname}:{lineno} | {message}',
            'style': '{',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'filters': ['correlation'],
        },
    },
    'filters': {
        'correlation': {
            '()': 'cid.log.CidContextFilter'
        },
    },
    'loggers': {
        LOGGER_ROOT_NAME: {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
            'filters': ['correlation'],
        },

        'general': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },

    },
}
# LOG SETUP END
