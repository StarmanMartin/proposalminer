 #!/bin/bash
cd /srv/app

printenv > .env

python ./__main__.py migrate

cron -f

