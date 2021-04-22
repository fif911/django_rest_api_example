FROM python:3.7-alpine
MAINTAINER Alex Zakotiasnkiy

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# needed reqs for postgres and pillow
RUN apk add --update --no-cache postgresql-client jpeg-dev
# these packeges only needed for installing pip
# so may be removed after installing reqs
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt
# removing them to save the space
RUN apk del .tmp-build-deps


RUN mkdir /app
WORKDIR /app
COPY ./app app

# create dirs for storing static and media
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
# give user perrmitions . -R means recursive
RUN chown -R user:user /vol/
RUN chown -R 755 /vol/web
USER user
