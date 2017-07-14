"""
Django settings for banner project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

#import os
import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'banner.settings'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8@)1%xo*sh_!gmb0)&z=&tsmaw#_6+!0%sidexy&t=g#6&052l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
SHOPIFY_MAX_RETRIES = 5
SHOPIFY_RETRY_WAIT=1
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'my_app',
	'shopify_auth',
	#'django_memcached',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'banner.urls'

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

# mezzanine hacks to works with django LTS (1.8.x)
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATES[0]['OPTIONS']['context_processors']
TEMPLATE_DIRS = TEMPLATES[0]['DIRS']

SILENCED_SYSTEM_CHECKS = (
  '1_8.W001'
)

WSGI_APPLICATION = 'banner.wsgi.application'

#def get_cache():
#  import os
#  try:
#    os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
#    os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
#    os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
#    return {
#      'default': {
#        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
#        'TIMEOUT': 500,
#        'BINARY': True,
#        'OPTIONS': { 'tcp_nodelay': True }
#      }
#    }
#  except:
#    return {
#      'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
#      }
#    }

#CACHES = get_cache()


CACHES = {
   'default': {
      'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
      'LOCATION': 'my_table_name',
   }
}
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'



# Configure Shopify Application settings
SHOPIFY_APP_NAME = 'Banner-Donate'
#SHOPIFY_APP_API_KEY = os.environ.get('41875187b83558c64926c744af853ec5')
SHOPIFY_APP_API_KEY = '622dd79c221f0a61fab4507e89d13aad'
#SHOPIFY_APP_API_SECRET = os.environ.get('8bacf8d2664ce3311e6c96dffe992ed6')
SHOPIFY_APP_API_SECRET = '161d5468074509c36e1639507b61b77a'
SHOPIFY_APP_API_SCOPE = ['read_products', 'read_orders', "read_script_tags", "write_script_tags"]
SHOPIFY_APP_IS_EMBEDDED = True
SHOPIFY_APP_DEV_MODE = False

# Use the Shopify Auth authentication backend as the sole authentication backend.
AUTHENTICATION_BACKENDS = (
    'shopify_auth.backends.ShopUserBackend',
)

# Add the Shopify Auth template context processor to the list of processors.
# Note that this assumes you've defined TEMPLATE_CONTEXT_PROCESSORS earlier in your settings.
TEMPLATE_CONTEXT_PROCESSORS += (
    'shopify_auth.context_processors.shopify_auth',
)

# Use the Shopify Auth user model.
AUTH_USER_MODEL = 'my_app.AuthAppShopUser'

# Set the login redirect URL to the "home" page for your app (where to go after logging on).
LOGIN_REDIRECT_URL = '/'

# Set secure proxy header to allow proper detection of secure URLs behind a proxy.
# This ensures that correct 'https' URLs are generated when our Django app is running behind a proxy like nginx, or is
# being tunneled (by ngrok, for example).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#import dj_database_url
#DATABASES = {'default': dj_database_url.config(default='postgres://cwanesywlmshgj:c60846281123be6e612300a0ce2ce2cc2bb03cabce0258eabad11d2a1cb00412@ec2-54-197-232-155.compute-1.amazonaws.com:5432/d7mcg5gu6u8o5f')}
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

import dj_database_url
DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

DEBUG = False

try:
    from .local_settings import *
except ImportError:
    pass
