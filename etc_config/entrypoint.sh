 #!/bin/bash
cd /srv/app

printenv > .env
./__main__.py migrate
cron -f

./manage.py initsuperuser
./manage.py build_all_oprator
daphne -b 0.0.0.0 -p 8000 ElnAdapter.asgi:application