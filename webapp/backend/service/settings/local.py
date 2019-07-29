from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True
    }
}

ALLOWED_HOSTS = ['*']
DEBUG = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'mysql.connector.django',
#         'NAME': "urf",
#         'USER': "admin",
#         'PASSWORD': "alex3412",
#         'HOST': "urf.chdthce697hh.us-east-1.rds.amazonaws.com",
#         'PORT': 3306,
#         'ATOMIC_REQUESTS': True,
#         'OPTIONS': {
#             'sql_mode': 'traditional',
#             'charset': 'utf8mb4'
#         }
#     },
# }
#
# DEBUG = True