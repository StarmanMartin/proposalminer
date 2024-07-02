 #!/bin/bash

 export $(xargs < /srv/app/.env)

 /usr/local/bin/python /srv/app/manage.py run_scheduled_processes