FROM python:3.7-alpine AS alpine-base

RUN apk add --no-cache python3 python3-dev gcc musl-dev zlib-dev libffi-dev openssl-dev ca-certificates

RUN pip3 install bottle requests asyncio aiohttp asyncio-throttle

RUN rm -fr /usr/local/lib/python3.7/site-packages/pip \
 && rm -fr /usr/local/lib/python3.7/site-packages/setuptools \
 && apk del python3-dev gcc musl-dev zlib-dev libffi-dev openssl-dev \
 && rm -rf /var/cache/apk/* /root/.cache /tmp/*

####################

FROM python:3.7-alpine

RUN set -ex \
    && apk add --no-cache bash

COPY --from=alpine-base /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages

RUN mkdir -pv \
     /epg \
     /epg/static_files/preprod \
     /epg/config

COPY web.py /epg/
COPY get_data.py /epg/
COPY settings.py /epg/config
COPY *.tpl /epg/
COPY entrypoint.sh /usr/sbin/entrypoint
RUN chmod 0777 /usr/sbin/entrypoint

CMD entrypoint "\5 \13 \* \* \* python3 /epg/get_data.py"

