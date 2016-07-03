FROM python:3.5
MAINTAINER Wojtek Pietrucha <wojtekpietrucha@gmail.com>
LABEL Description="This image is used to start the grortir app." Version="1.0"
RUN git clone https://github.com/qbahn/grortir.git /src/usr/grortir
WORKDIR /src/usr/grortir
RUN apt-get update
RUN cat ./required-system-packages.txt | xargs apt-get install -y
RUN make