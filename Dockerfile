FROM gliderlabs/alpine

MAINTAINER Henry Cooke <me@prehensile.co.uk>

# update system
RUN apk update && apk upgrade

# build frotz
COPY ./frotz /usr/local/src/frotz
WORKDIR /usr/local/src/frotz
RUN apk add build-base
RUN export CFLAGS=-fPIC && make clean && make dumb \
    && mkdir -p /app/frotz && cp /usr/local/src/frotz/dfrotz /app/frotz/dfrotz \ 
    && chmod +x /app/frotz/dfrotz && rm -rf /usr/local/src/frotz

# install python
RUN apk add python py-pip

# copy python requirements into container
COPY ./requirements.txt /app/requirements.txt

# install python requirements in container
WORKDIR /app
RUN pip install -r /app/requirements.txt && rm /app/requirements.txt

# copy app code into container
ADD ./app /app

EXPOSE 8080

# entry point
CMD "/app/main.py"