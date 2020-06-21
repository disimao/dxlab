FROM python:3.8.3-buster 

USER root

ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY . /src/

RUN apt-get upgrade

RUN apt-get -qq -y update && \
	apt-get -qq -y install \
        python3-pip && \
    apt-get -y autoclean && \
    apt-get -y autoremove 

RUN apt-get -qq -y install \
	python-mysqldb

RUN apt-get -qq -y install \
    default-libmysqlclient-dev

ADD ./requirements/production.txt /requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir static

VOLUME ["/static"]

WORKDIR /src

EXPOSE 8000
