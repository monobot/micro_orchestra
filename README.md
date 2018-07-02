# micro_orchestra
## Test for 3 microservices communicating

3 docker microservices communication throught a redis docker instance.

Using my own library redis_connector

Each of the microservices will be able to process its own messages, and will be connecting to the list of channels.
Each message will be processed only once using the redis lock feature.
So you can scalate up any of the microservices without worring about the concurrence.

eg:
docker-compose up --scale final_box=3 processor_box=2
