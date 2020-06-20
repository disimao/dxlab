FROM centos/python-38-centos7 

USER root

ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY . /src/

ADD ./requirements/prod.txt /requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir static

VOLUME ["/static"]

WORKDIR /src

EXPOSE 8000
