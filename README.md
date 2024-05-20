# coralpayroll
accounting payroll website

## WINDOWS ##
create a virtual environment

`$pyhton3 -m venv .venv`

__activate the virtual environmnet__

`.venv\Scripts\activate`

__activate the virtual environment LINUX__

`source ./venv/bin/activate`

__install the package__

`python -m pip install django`

`python -m pip install python-dotenv`

 __postgress windows__

`pip install psycopg2`

__postgress linux__

`pip install psycopg2-binary`

`pip install django-bootstrap-v5`

`pip install django-crispy-forms`

`pip install crispy-bootstrap5`

`pip install whitenoise`

`pip install sqlalchemy`

`pip install gunicorn`

colect static result:

`pip install django-encrypted-model-fields`

create the .env file at ./coral_payroll/coral_payroll
and fill this variables:

SECRET_KEY = 'django-insecure-yy_@v%r(2$ti36atw8#^ycho7ue&@)4l!ig+i=h0r0w$8hyj!v'
DEBUG = True
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
SUPERUSER=''
SUPERUSER_PASSWORD=''
SUPERUSER_EMAIL=''
ALLOWED_HOSTS = ''
FIELD_ENCRYPTION_KEY = ''

`sudo ufw allow port/udp`

`sudo ufw allow port/tcp`

run gunicorn

gunicorn --bind 0.0.0.0:8009 your_project_name.wsgi:application

https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/gunicorn/

TODO:
 - Calculos por cuatrimestre
 
Static files are at: 
.\coralpayroll_project\accounts\static