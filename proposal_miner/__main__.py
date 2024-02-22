import sys

from app import run
from db_manager import run_django_cmd

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_django_cmd()
    else:
        run(config_path='../config.ini')