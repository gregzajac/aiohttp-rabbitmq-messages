FROM python:3.6-slim

WORKDIR /usr/src/app 

ADD . /usr/src/app

RUN pip3.6 install --no-cache-dir -r requirements.txt

CMD python run.py