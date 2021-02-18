FROM in-toto-python:demo
LABEL maintainer="Carlos OKieffe <okieffe_carlos@bah.com>"

COPY ./porter porter

RUN apk add curl

# now adding porter stuff
RUN porter/install-porter.sh
ENV PORTER_HOME=/root/.porter

# end porter stuff

# signy stuff
# needs go lang
COPY --from=golang:1.15-alpine /usr/local/go/ /usr/local/go/
RUN apk add git make

ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/opt/go/"

RUN mkdir -p $GOPATH/bin
RUN mkdir -p $GOPATH/src/github.com
WORKDIR $GOPATH/src/github.com
RUN mkdir cnabio && cd cnabio && git clone https://github.com/cnabio/signy && cd signy
ENV SIGNY_HOME=$GOPATH/src/github.com/cnabio/signy
WORKDIR $SIGNY_HOME
RUN make bootstrap build
RUN cp $SIGNY_HOME/bin/signy $GOPATH/bin
