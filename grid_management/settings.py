"""
Django settings for grid_management project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wb*8adc^8@m0-@9=-gm!-jlq92fz52(xsa#v8drotbize*@&63'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

'''LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
       'file': {
           'level': 'DEBUG',
           'class': 'logging.FileHandler',
           'filename': 'log.django',
       },
    },
    'loggers': {
        'django': {
            'handlers': ['console','file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}'''
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'resident',
    'grid',
    'index',
    'core',
    'api',
    'notifications',
    'notifications_rest',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True 

ROOT_URLCONF = 'grid_management.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates')),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.NavbarTabs',
                'core.context_processors.get_sitetitle',
				'core.context_processors.get_headInfo',
                'core.context_processors.get_footInfo',
                'core.context_processors.get_version',
                'core.context_processors.is_inviteRegOnly',
                'core.context_processors.is_underMaintaining',
                'core.context_processors.get_live_user_approval_count',
                'core.context_processors.get_map_key',
                'core.context_processors.get_map_style_id',
                'core.context_processors.get_live_static_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'grid_management.wsgi.application'

DJANGO_NOTIFICATIONS_CONFIG = { 'SOFT_DELETE': True}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default="postgres://hpfcszkxsihiom:794c0dd0e9de2c242fa401f5f3024e594144892c2a064ebb4dfee073a8cf240e@ec2-44-207-253-50.compute-1.amazonaws.com:5432/dbbd571lbsf9qd")
    }

'''DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': BASE_DIR / 'db.sqlite3',
    #}
    'default':{
    'ENGINE':'django.db.backends.postgresql_psycopg2',
    'NAME':'grid_management',
    'USER': 'postgres',
    #'PASSWORD': str(os.environ.get('DBPASSWD',True)),
    'PASSWORD': 'FireAndSw0rd1',
    'HOST': 'localhost',
    'PORT': '5432',
    }
}'''


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ('en', ('English')),
    ('zh-hans', ('中文简体')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [
    ('css', os.path.join(STATIC_ROOT, 'css')),
    ('js', os.path.join(STATIC_ROOT, 'js')),
    ('webfonts', os.path.join(STATIC_ROOT, 'webfonts')),
    ('img', os.path.join(STATIC_ROOT, 'img')),
    #('font', os.path.join(STATIC_ROOT, 'font')),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
