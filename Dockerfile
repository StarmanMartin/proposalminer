FROM python:3.13-slim
LABEL authors="martin"
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /srv/app

WORKDIR /srv/app

RUN apt-get update && apt-get install -y cron nano libmagic1

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install typing-extensions

COPY ./config.ini.sample ../config.ini
COPY ./proposal_miner .
COPY ./etc_config/cron_entrypoint.sh /srv/app/cron_entrypoint.sh
COPY ./etc_config/entrypoint.sh /srv/app/entrypoint.sh
RUN chmod +x /srv/app/cron_entrypoint.sh
RUN chmod +x /srv/app/entrypoint.sh

RUN touch /var/log/cron.log

#RUN echo "SHELL=/bin/bash" > /etc/cron.d/my_custom_cron
#RUN echo "PATH=/sbin:/bin:/usr/sbin:/usr/bin" >> /etc/cron.d/my_custom_cron

RUN echo "*/10 * * * * bash -c '/srv/app/cron_entrypoint.sh' >> /var/log/cron.log 2>&1" > /etc/cron.d/my_custom_cron

RUN chmod 0644 /etc/cron.d/my_custom_cron
RUN /usr/bin/crontab /etc/cron.d/my_custom_cron

RUN service cron start

ENTRYPOINT ["bash", "/srv/app/entrypoint.sh"]