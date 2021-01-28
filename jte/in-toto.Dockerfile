FROM alpine:latest
LABEL maintainer="Carlos OKieffe <okieffe_carlos@bah.com>"

ENV PYTHONUNBUFFERED=1
RUN apk update && apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN apk add git
#for gcc which is needed for pip cryptography
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

# FIXME: colorama shouldn't be there, but the upstream dependency is broken
# until the next release.
#RUN pip3 install --upgrade pip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN pip3 install cryptography securesystemslib[crypto] in-toto 

RUN mkdir /workspace
WORKDIR /workspace
COPY . demo
