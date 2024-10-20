import os
from pathlib import Path
from corsheaders.defaults import default_headers
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")  # Add fallback if not set

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'  # Set to False for production

# Allowed hosts configuration
# Add 'myproject-00vc.onrender.com' to ALLOWED_HOSTS for production
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost myproject-00vc.onrender.com").split(" ")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ssis',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

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

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database configuration with fallback
# database_url = os.environ.get("DATABASE_URL")
# DATABASES = {
#     'default': dj_database_url.parse(database_url or "postgres://user:password@localhost/dbname")
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",  # or your database name
        "USER": "postgres.yqoixhmtlymgapjtobzn",
        "PASSWORD": os.environ.get('DB_PASSWORD', 'mlekwa@@123'),
        "HOST": "aws-0-us-west-1.pooler.supabase.com",
        "PORT": "6543",
        "OPTIONS": {
            'sslmode': 'require',  # Require SSL for the connection
        }
    }
}

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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = 'ssis.UserTB'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://ssis-d1204.web.app",
    "https://myproject-00vc.onrender.com"
    "http://localhost:3000/"
]
CORS_ALLOW_HEADERS = list(default_headers) + [
    'content-disposition',
]

CORS_ALLOW_ALL_ORIGINS = DEBUG  # Allow all origins in development only

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
