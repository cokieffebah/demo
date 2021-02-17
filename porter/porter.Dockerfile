FROM in-toto-python:demo
LABEL maintainer="Carlos OKieffe <okieffe_carlos@bah.com>"

COPY ./porter porter

RUN apk add curl

# now adding porter stuff
RUN ./porter/install-porter.sh

# end porter stuff