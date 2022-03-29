"""
Django settings.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

import environ
import structlog

env = environ.FileAwareEnv(
    # set casting, default value
    DEBUG=(bool, False),
    ENVIRONMENT=(str, "dummy"),  # see section if env("ENVIRONMENT") == "local"
    DB_HOST=(str, "cockroach"),
    DB_PORT=(str, "26257"),
    DB_NAME=(str, "defaultdb"),
    AWS_ACCESS_KEY_ID_BACKEND=(str, "dummy"),
    AWS_SECRET_ACCESS_KEY_BACKEND=(str, "dummy"),
    GOOGLE_APPLICATION_CREDENTIALS=(str, "{}"),
    GOOGLE_ANALYTICS_GTAG_PROPERTY_ID=(str, "dummy"),
)

BASE_DIR = Path(__file__).resolve().parent.parent
environ.FileAwareEnv.read_env(os.path.join(BASE_DIR, env.str("ENV_PATH", ".env")))

COMPANY_NAME = "Cloud Outdated"
BASE_URL_ENVS = {
    "local": "http://localhost",
    "dev": "https://dev.cloud-outdated.com",
    "prod": "https://cloud-outdated.com",
}
BASE_URL = BASE_URL_ENVS[env("ENVIRONMENT")]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

OPERATORS_EMAIL = [
    # "liezun.js@gmail.com",
    "mislav.cimpersak@gmail.com",
]

RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")
RECAPTCHA_REQUIRED_SCORE = 0.85

ALLOWED_HOSTS = [
    "dev.cloud-outdated.com",
    "www.cloud-outdated.com",
    "cloud-outdated.com",
    "b4eu57c6a2.execute-api.eu-central-1.amazonaws.com",  # dev
    "4r4hbnvvu8.execute-api.eu-central-1.amazonaws.com",  # prod
    "127.0.0.1",
    "localhost",
]

DATABASES = {
    "default": {
        "ENGINE": "django_cockroachdb",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

# Application definition
INSTALLED_APPS = [
    "django_admin_env_notice",  # must come before django.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "analytical",
    "anymail",
    "captcha",
    "core",
    "notifications",
    "services",
    "subscriptions",
    "users",
]

# used by SES
# poll_aws uses zappa managed role
# default names are overriden and set by Lambda and Zappa
AWS_ACCESS_KEY_ID_BACKEND = env("AWS_ACCESS_KEY_ID_BACKEND")
AWS_SECRET_ACCESS_KEY_BACKEND = env("AWS_SECRET_ACCESS_KEY_BACKEND")

DEFAULT_FROM_EMAIL = "cloudoutdated@gmail.com"

EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"

ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "aws_access_key_id": AWS_ACCESS_KEY_ID_BACKEND,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY_BACKEND,
        "region_name": "eu-central-1",
    }
}

# used for polling GCP services
GOOGLE_APPLICATION_CREDENTIALS = env("GOOGLE_APPLICATION_CREDENTIALS")

LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # used by Django admin
    "sesame.backends.ModelBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "sesame.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
]

SESAME_MAX_AGE = 60 * 24 * 2  # in seconds
SESAME_TOKEN_NAME = "magic"

# dev in this path is name of deployment env,
# will probably be just `/static/` when deploying to {env}.domain.com
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# not using whitenoise storage engine because of some issue with lambda
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
WHITENOISE_STATIC_PREFIX = "/static/"

ROOT_URLCONF = "cloud_outdated.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django_admin_env_notice.context_processors.from_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "cloud_outdated.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.UserProfile"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "console_json": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console_json"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Service polling configurations
POLLING_THREADS = 4
NOTIFICATIONS_MAX_RETRIES = 10
NOTIFICATIONS_MAX_TIME = 60 * 5

GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = env("GOOGLE_ANALYTICS_GTAG_PROPERTY_ID")

# django-admin-env-notice
ENVIRONMENT_NAME = env("ENVIRONMENT")
if env("ENVIRONMENT") == "local":
    ENVIRONMENT_COLOR = "#5F9EA0"
elif env("ENVIRONMENT") == "dev":
    ENVIRONMENT_COLOR = "#228B22"
elif env("ENVIRONMENT") == "prod":
    ENVIRONMENT_COLOR = "#C04000"
else:
    ENVIRONMENT_COLOR = "#000000"

# local overrides
if env("ENVIRONMENT") == "local":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
