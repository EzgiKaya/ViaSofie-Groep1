#Django 1.9.4.

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR=os.path.dirname(__file__)

# SECURITY WARNING: keep the secret key used in production secret!
#capthca
SECRET_KEY = 'l$=u-!l5n8c-(795ugc@5(o(yz9g26*pmdou*@@)dzuqcc5iws'
NORECAPTCHA_SITE_KEY = '6LdwqCATAAAAABx3v-fnrR_equMwX8U7PD7Ka9f2'
NORECAPTCHA_SECRET_KEY = '6LdwqCATAAAAALqeH_tb9HlRWx2tiEXXqwnNa3pC'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Application definition
# Geinstalleerde apps voor werkende functionaliteiten binnenin de webapplicatie
INSTALLED_APPS = [
    'websiteSofie.apps.websiteSofieConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3', # bootstrap3 opmaak
    'nocaptcha_recaptcha', # captcha
    'django.contrib.humanize', # opmaak voor valuta
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]


ROOT_URLCONF = 'websiteSofie.urls'

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

WSGI_APPLICATION = 'websiteSofie.wsgi.application'

# Database
# database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vastgoed',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Media settings
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"

# Password validation

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

# Server taal
LANGUAGE_CODE = 'nl-BE'

# Beschikbare talen voor vertalingen, voeg hier talen toe om deze beschikbaar te stellen voor de site.
# Deze moeten nog vertaald worden binnen de locale folder in de bijhorende .po bestand.
LANGUAGES = [
    ('nl', _('Nederlands')),
    ('en', _('Engels')),
]

# Folder waar vertalingsbestanden opgeslaan worden als .po and .mo bestanden
LOCALE_PATH = [
    '/locale',
]

# Tijdszone en vertalingsconventie instellingen
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, "static")

# Login
LOGIN_URL = '/websiteSofie/login'

# Mailserver instellingen
DEFAULT_FROM_EMAIL = 'Via Sofie <viasofiegroep1@gmail.com>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'viasofiegroep1@gmail.com'
EMAIL_HOST_PASSWORD = 'testgroep1'
EMAIL_PORT = 587
