from os import environ

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': environ.get('DATABASE_NAME', './db.sqlite3'),
        'USER': environ.get('DATABASE_USER'),
        'PASSWORD': environ.get('DATABASE_PASSWORD'),
        'HOST': environ.get('DATABASE_HOST'),
        'PORT': environ.get('DATABASE_PORT'),
    }
}
