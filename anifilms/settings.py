from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%5#y4&-vxl%5w2#)a0-rvcbp59t_q+=gbl01&tfisa&*q9m^3+5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


if DEBUG == True:
    from dotenv import load_dotenv
    load_dotenv()



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ###---- librrary ----###
    
    'storages',
    'crispy_forms',
    'taggit',
    'comment.apps.CommentConfig',
    'rating.apps.RatingConfig',
    
    ###---- local ----###
    'anim',
    'user',
    'control_panel',
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

SITE_ID = 1
LOGOUT_REDIRECT_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'anime:list'
ROOT_URLCONF = 'anifilms.urls'
LOGIN_URL = 'accounts:login' 


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

WSGI_APPLICATION = 'anifilms.wsgi.application'
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"


USE_I18N = True
USE_L18N = True
LANGUAGE_CODE = 'fa-ir'


COMMENT_SETTINGS = {
    # generated urlhash length
    'URLHASH_LENGTH': 8,

    # if True, tailwindcss and jquery package will be loaded from static files.
    'OFFLINE_IMPORTS': False,
    # if None, comments will be shown without profile image
    # you should set this value as profile image field name
    # for example our abstract user profile picture field is profile_image
    # <img src="{{ user.profile_image.url }}" /> so we set PROFILE_IMAGE_FIELD = 'profile.image'
    # see link blew to create abstract user model
    # https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model
    'PROFILE_IMAGE_FIELD': 'user.photo',
}

RATING_SETTINGS = {
    # generated urlhash length
    'URLHASH_LENGTH': 8
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
# 		'NAME': BASE_DIR / 'db.sqlite3',
# 	}
# }

DATABASES = {
 'default': {
     'ENGINE': 'django.db.backends.postgresql',
     'NAME': os.getenv("sql_NAME"),
     'USER': os.getenv("sql_USER"),
     'PASSWORD': os.getenv("sql_PASSWORD"),
     'HOST': os.getenv("sql_HOST"),
     'PORT': os.getenv("sql_PORT"),
 }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L18N = True




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')

MEDIA_ROOT = ''
MEDIA_URL = os.path.join(BASE_DIR, '/media/')


STATICFILES_LOCATION = os.path.join(BASE_DIR, '/static/')


AWS_LOCATION = 'static'

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_USE_TLS = True  
# EMAIL_HOST = 'smtp.gmail.com'  
# EMAIL_HOST_USER = 'email@gmail.com'  
# EMAIL_HOST_PASSWORD = 'password'  
# EMAIL_PORT = 587  


# S3 Settings
LIARA_ENDPOINT    = os.getenv("LIARA_ENDPOINT")
LIARA_BUCKET_NAME = os.getenv("LIARA_BUCKET_NAME")
LIARA_ACCESS_KEY  = os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY  = os.getenv("LIARA_SECRET_KEY")

AWS_ACCESS_KEY_ID = LIARA_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = LIARA_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = LIARA_BUCKET_NAME
AWS_S3_ENDPOINT_URL = LIARA_ENDPOINT
AWS_S3_REGION_NAME = 'us-east-1'  

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

# Django-storages configuration
STORAGES = {
    "default": {
        "BACKEND": "anifilms.s3utils.MediaStorage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}
