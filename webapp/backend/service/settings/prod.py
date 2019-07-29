from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': "urf",
        'USER': "admin",
        'PASSWORD': "alex3412",
        'HOST': "urf.chdthce697hh.us-east-1.rds.amazonaws.com",
        'PORT': 3306,
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'sql_mode': 'traditional'
        }
    },
}
use_charset = os.environ.get("use_utf8mb4", True)
if use_charset != '0':
    DATABASES['default']['OPTIONS']['charset'] = 'utf8mb4'

DEBUG = True
