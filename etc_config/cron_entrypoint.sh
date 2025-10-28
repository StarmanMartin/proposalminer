#!/bin/bash

export $(xargs -0 < /srv/app/.env)

cd /srv/app
/usr/local/bin/python /srv/app/__main__.py