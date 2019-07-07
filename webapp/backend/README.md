## Install
1. Create virtualenv
2. `pip install -r requirements.txt`

## Initial deployment static files for swagger
1. `python manage.py collectstatic --noinput`
2. `zappa deploy`

## Updates
1. `zappa update`

## DB Migrations
`zappa manage prod migrate app zero` (Rolls all migrations back for a fresh start)

`zappa manage prod migrate`