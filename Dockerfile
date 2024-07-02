FROM python:3.10
LABEL authors="martin"
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /srv/app

WORKDIR /srv/app

RUN apt-get update && apt-get install -y cron nano

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mv /srv/app/etc_config/cron_entrypoint.sh /srv/app/cron_entrypoint.sh
RUN chmod +x /srv/app/cron_entrypoint.sh
RUN chmod +x /srv/app/entrypoint.sh

RUN touch /var/log/cron.log

#RUN echo "SHELL=/bin/bash" > /etc/cron.d/my_custom_cron
#RUN echo "PATH=/sbin:/bin:/usr/sbin:/usr/bin" >> /etc/cron.d/my_custom_cron

RUN echo "/1 * * * * bash -c '/srv/app/cron_entrypoint.sh' >> /var/log/cron.log 2>&1" > /etc/cron.d/my_custom_cron

RUN chmod 0644 /etc/cron.d/my_custom_cron
RUN /usr/bin/crontab /etc/cron.d/my_custom_cron

RUN mkdir /srv/app/node_modules
RUN mkdir /srv/app/static
RUN service cron start

CMD ["cron", "-f"]