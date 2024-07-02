 #!/bin/bash

 export $(xargs -0 < /srv/app/.env)

 /usr/local/bin/python /srv/app/__main__.py