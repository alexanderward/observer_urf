DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "urf",
        'USER': "admin",
        'PASSWORD': "alex3412",
        'HOST': "urf.cluster-chdthce697hh.us-east-1.rds.amazonaws.com",
        'PORT': 3306,
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
}