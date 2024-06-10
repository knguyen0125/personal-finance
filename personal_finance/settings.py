from django.utils.translation import gettext_lazy as _
import environ
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
env.read_env(str(BASE_DIR / ".env"))

SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "rest_framework",
    "slippers",
    "pf_account",
    "pf_accounting",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "personal_finance.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["slippers.templatetags.slippers"],
        },
    },
]

WSGI_APPLICATION = "personal_finance.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": env.db(),
}

CACHES = {
    "default": env.cache(),
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
AUTH_USER_MODEL = "pf_account.User"

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

LANGUAGES = [
    ("en", _("English")),
    ("vi", _("Vietnamese")),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_HOST = env.str("STATIC_HOST", default="")
STATIC_URL = STATIC_HOST + "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if env.bool("USE_S3", default=False):
    MEDIA_STORAGE = "storages.backends.s3.S3Storage"
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    if env.str("AWS_ACCESS_KEY_ID"):
        AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
        AWS_SESSION_TOKEN = env.str("AWS_SESSION_TOKEN", default=None)
    AWS_S3_CUSTOM_DOMAIN = env.str("AWS_S3_CUSTOM_DOMAIN", default=None)
    AWS_CLOUDFRONT_KEY = env.str("AWS_CLOUDFRONT_KEY", default=None)
    AWS_CLOUDFRONT_KEY_ID = env.str("AWS_CLOUDFRONT_KEY_ID", default=None)
else:
    MEDIA_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_HOST = env.str("MEDIA_HOST", default="")
    MEDIA_URL = MEDIA_HOST + "/media/"

STORAGES = {
    "default": {
        "BACKEND": MEDIA_STORAGE,
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

EMAIL_CONFIG = env.email()

vars().update(EMAIL_CONFIG)
