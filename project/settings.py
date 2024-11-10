"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--fq(@un1_5#&qg9-916ymc4g%mk$n-l!2-n5m=tp3v2^_lo99a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # all-auth api
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',


    # My Packages
    'taggit',
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'debug_toolbar',
    'bootstrap5',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth',

    # My Apps
    'products.apps.ProductsConfig',
    'settings.apps.SettingsConfig',
    'orders.apps.OrdersConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Add translation middleware
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'settings.settings_context_processors.settings_data',
                'orders.cart_context_processor.get_cart_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "amazon",
#         "USER": "postgres_user",
#         "PASSWORD": "2925",
#         "HOST": "db",
#         "PORT": "5432",
#     }
# }

# Redis caching
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # Redis URL and DB number for docker
        # 'LOCATION': 'redis://127.0.0.1:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Celery & Redis
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_BACKEND_RESULTS = 'redis://localhost:6379'

# Celery in Docker
# Celery & Redis
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_BACKEND_RESULTS = 'redis://redis:6379/0'


# Rest API Settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
}
SITE_ID = 1


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'tr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Debug tool
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# For loggin with emails also not just in usernames
AUTHENTICATION_BACKENDS = [
    'accounts.backend.EmailOrUsernameLogin',
]

# For sending emails
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "ismekbektop@gmail.com"
EMAIL_HOST_PASSWORD = "pogqkisnkxdwveyu"


# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

# Payments settings
STRIPE_API_KEY_PUBLISHABLE = 'pk_test_51PqcbcFFXmaIAdi3Hnw3TsmAAYsWsH1HCYzq65aQ0UxN6VXq5jfrkhu19mvWd0t7If2G4yYvn0DqUyaWfnWLYP3g00dBoLOXAI'
STRIPE_API_KEY_SECRET = 'sk_test_51PqcbcFFXmaIAdi3ONZ73ioWSgzpGIdlSzxfvNH0fvbZqfFBfehvz8pwsT330Bm2pO1lCNAkIlGM8iazBrGAq0RP00M6LCtHPn'

# Translation
LOCALE_PATHS = [
    "locale",
]

LANGUAGES = (
    ('en', 'English'),
    ('tr', 'Turkish'),
    ('ar', 'Arabic')
)
