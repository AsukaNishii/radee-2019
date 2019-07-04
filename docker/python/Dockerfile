FROM python:3.5-alpine

RUN apk add g++ libc-dev python3-dev linux-headers && \
    pip install --upgrade pip && \
    pip install flask numpy scipy matplotlib && \
    pip install --no-cache-dir --no-build-isolation pandas

WORKDIR /home/radee2019
