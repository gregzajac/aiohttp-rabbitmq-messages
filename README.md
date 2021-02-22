# Async messages queuing (AioHTTP+SQlite3 and RabbitMQ)

Solution composed of two async AioHTTP servers and message broker RabbitMQ:
1. Server A (front-server) with REST API managing two endpoints
field 1 | field 2 | field 3
------- | ------- | -------
desc 1 | desc 2 | desc 3


  endpoint  |  method  |  input  |  output  |  example
  --------  |  ------  |  -----  |  ------  |  -------
  http://localhost:8080/api  |  POST  |  JSON {key:value}, key(str), value(int/float)  |  JSON {'message':boolean, data/message: string}  |  curl -i -X POST -H "Content-Type: application/json" -d '{"age":25}' http://localhost:8080/api
  http://localhost:8080/api  |  GET  |  attribute key in URL  |  JSON {'message':boolean, data/message: string}  |  curl -i http://localhost:8080/api?key=age


REST API validates input data, in case of error returns an apriopriate HTTP error in JSON output. Validated data are trasferred to message broker (RabbitMQ). 
Server HTTP manages tasks in asynchonous way.

2. Message broker RabbitMQ, managing messages between two servers (one direction in POST case, two directions in GET case).

3. Server B (back-server) with database SQlite3, retrieves messages from message broker and saves (POST method) or gets (GET method) data from the database. 
In case of GET method Server B transfers obtaining value from the database to the message broker. In case of retrieving message with key existing in the database, Server B updates the old value with the new one. Server runs in asynchronous way handling broker and database connections and operations. SQlite3 database includes one table (ID (pk), KEY (unique text), VALUE (float)).


## Setup (on linux)

- Clone repository
- Create docker images of front-server and back-server solutions
```buildoutcfg
# example of creating images from directories with Dockerfile
sudo docker build -t frontserver:0.1 .
sudo docker build -t backserver:0.1 .
```
- Run rabbitmq image (local rabbitmq if exists should be turned off: *service rabbitmq-server stop*)
```buildoutcfg
sudo docker run -d -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```
- Run servers images
```buildoutcfg
sudo docker run -it -p 8080:8080 frontserver:0.1
sudo docker run -it backserver:0.1
```

### NOTE

For closing environments stop running docker containers
```buildoutcfg
# checking running containers
sudo docker ps

#closing fixed container
sudo docker stop <container_name>
```


## Technologies / Tools

- Python 3.6.8
- Aiohttp 3.7.3
- Aio-pika 6.8.0
- Aiosqlite 0.16.1
- PyYAML 5.4.1
- Sqlite3
- RabbitMQ
- Docker


