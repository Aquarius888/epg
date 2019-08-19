FROM python:3.6-alpine

RUN set -ex \
    && apk add --no-cache \
    bash

RUN mkdir -pv \
     /epg \
     /epg/static_files \
     /epg/config

RUN pip3 install bottle requests

COPY web.py /epg/
COPY get_data.py /epg/
COPY settings.py /epg/config
COPY *.tpl /epg/
COPY entrypoint.sh /usr/sbin/entrypoint
RUN chmod 0777 /usr/sbin/entrypoint

CMD entrypoint "\5 \13 \* \* \* python3 /epg/get_data.py"

