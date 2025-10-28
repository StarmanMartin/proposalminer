import sys

from app import run
from db_manager import run_django_cmd
from orm.clean import clean_all


def run_cmd():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'clean':
            fp = sys.argv[2] if len(sys.argv) > 2 else None
            clean_all(fp)
        else:
            run_django_cmd()
    else:
        run(config_path='../config.ini')


if __name__ == '__main__':
    run_cmd()
