FROM python:3-alpine

#Discord server webhook URL
#ENV DISCORD_URL=""

#Pushover Tokens
#ENV API_TOKEN=""
#ENV USER_TOKEN=""

#Python set work dir
ENV DIRPATH=/rfd-push
WORKDIR /rfd-push

COPY ./crontab.txt /rfd-push/crontab.txt
COPY ./script.sh /rfd-push/script.sh
COPY ./newdealchecker.py /rfd-push/newdealchecker.py

RUN chmod 755 /rfd-push/script.sh
RUN /usr/bin/crontab /rfd-push/crontab.txt

# Script file

# Entrypoint
COPY ./entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh

#Install dependencies
RUN pip3 install --upgrade pip setuptools==57.5.0

COPY ./requirements.txt /rfd-push/requirements.txt

#Download rfd
RUN pip3 install -r requirements.txt

###rfdpath=/usr/local/bin/rfd

ENTRYPOINT [ "entrypoint.sh" ]
