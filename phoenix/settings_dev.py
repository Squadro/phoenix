from .settings_common import *  # noqa

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    },
    # 'read_replica': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': os.environ.get('POSTGRES_DBNAME'),
    #         'USER': os.environ.get('POSTGRES_USER'),
    #         'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    #         'HOST': os.environ.get('POSTGRES_HOST'),
    #         'PORT': os.environ.get('POSTGRES_PORT'),
    #
    #     }
    "read_replica": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bonito",
        "USER": "bonito",
        "PASSWORD": "RG]pn2W^'<(7",
        "HOST": "bonito-app-rds-read-replica.cnxne33fjape.ap-south-1.rds.amazonaws.com",
        "PORT": "5432",
    },
}
