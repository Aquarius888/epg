FROM python:3.6-alpine

RUN set -ex \
    && apk add --no-cache \
    bash

RUN mkdir -pv \
     /epg \
     /epg/static_files

RUN pip3 install bottle requests

COPY *.py /epg/
COPY *.tpl /epg/
COPY entrypoint.sh /usr/sbin/entrypoint
RUN chmod 0777 /usr/sbin/entrypoint

CMD entrypoint "\5 \13 \* \* \* python3 /epg/get_data.py"

