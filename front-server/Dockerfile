FROM python:3.6-slim

WORKDIR /usr/src/app 

ADD . /usr/src/app

RUN pip3.6 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD gunicorn 'api:create_app()' -b :8080 --worker-class aiohttp.GunicornWebWorker --timeout 120 --reload --access-logfile -
