import os
import sys
import django
from django.conf import settings

BASE_DIR =  os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = [
    'orm',
]

DATABASES = {
    'default':  {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'proposal.sqlite3', # This is where you put the name of the db file.
        # If one doesn't exist, it will be created at migration time.
    }
}

settings.configure(
    BASE_DIR=BASE_DIR,
    INSTALLED_APPS = INSTALLED_APPS,
    DATABASES = DATABASES,
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
)

def setup():
    django.setup()

def run_django_cmd():
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    run_django_cmd()

__all__ = ['setup','run_django_cmd']