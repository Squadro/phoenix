from .settings_common import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ["aws.com", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "phoenix_staging",
        "USER": "postgres",
        "PASSWORD": "Bonito1234",
        "HOST": "phoenix-staging-instance-1.cnxne33fjape.ap-south-1.rds.amazonaws.com",
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
