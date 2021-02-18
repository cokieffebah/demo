FROM in-toto-python:demo
LABEL maintainer="Carlos OKieffe <okieffe_carlos@bah.com>"

COPY ./porter porter

RUN apk add curl ca-certificates

# zscaler at bah
RUN cp porter/certs/* /usr/local/share/ca-certificates && \
    chmod 644 /usr/local/share/ca-certificates/* && \
    update-ca-certificates

# now adding porter stuff
#RUN echo insecure >> ~/.curlrc #having issue with porter curl

RUN porter/install-porter.sh
ENV PORTER_HOME=/root/.porter

# end porter stuff

# signy stuff
# needs go lang
COPY --from=golang:1.15-alpine /usr/local/go/ /usr/local/go/
RUN apk add git make docker

ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/workspace/go/"

RUN mkdir -p $GOPATH/bin
RUN mkdir -p $GOPATH/src/github.com
WORKDIR $GOPATH/src/github.com
RUN mkdir cnabio && cd cnabio && git clone https://github.com/cnabio/signy && cd signy
ENV SIGNY_HOME=$GOPATH/src/github.com/cnabio/signy
WORKDIR $SIGNY_HOME
RUN make bootstrap build
RUN cp $SIGNY_HOME/bin/signy $GOPATH/bin
