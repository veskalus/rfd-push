#FROM alpine:latest
FROM python:3-alpine

#Python set work dir
#WORKDIR /usr/src/app
ENV DIRPATH=/rfd-push
WORKDIR $DIRPATH

ENV SEARCH_TERM="(wd|dji|12tb)"
ENV API_TOKEN=""
ENV USER_TOKEN=""

#RUN apk update \
#    && apk add cron

# Cron file
#ADD ./my-cron /etc/cron.d/my-cron
#RUN chmod 0644 /etc/cron.d/my-cron

COPY ./crontab.txt $DIRPATH/crontab.txt
COPY ./script.sh $DIRPATH/script.sh
COPY ./newdealchecker.py $DIRPATH/newdealchecker.py

RUN chmod 755 $DIRPATH/script.sh

RUN /usr/bin/crontab $DIRPATH/crontab.txt

# Script file

# Entrypoint
COPY ./entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh

#RUN apk update

#install dependencies
RUN pip3 install --upgrade pip setuptools==57.5.0

COPY ./requirements.txt $DIRPATH/requirements.txt

#Download rfd
RUN pip3 install -r requirements.txt

###rfdpath=/usr/local/bin/rfd


ENTRYPOINT [ "entrypoint.sh" ]


