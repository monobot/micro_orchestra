#!/usr/bin/env python
import uuid

from redis_connector import RedisConnector


HOST = 'redis_cache'
PORT = 6379
QUEUENAME = 'microservices'
QUEUES = [QUEUENAME, ]
MICRO_SERVICE_NAME = 'publisher'

redis_connector_publisher = RedisConnector(HOST, PORT, QUEUES, MICRO_SERVICE_NAME)
t = 1
while True:
    message = {
        "target": 'processor',
        "message_id": str(uuid.uuid4()),
        "message": "Bingo {}".format(t),
        "data": {
            'first': t,
            'operation': '+',
            'second': t,
        }
    }
    redis_connector_publisher.publish(QUEUENAME, message)
    t += 1
    processor_instances = redis_connector_publisher.publish(
        'ping:processor',
        {"message": "ping"}
    )
    final_instances = redis_connector_publisher.publish(
        'ping:final',
        {"message": "ping"}
    )
    publisher_instances = redis_connector_publisher.publish(
        'ping:publisher',
        {"message": "ping"}
    )
    print('publisher_instances: {}'.format(publisher_instances))
    print('processor_instances: {}'.format(processor_instances))
    print('final_instances: {}'.format(final_instances))
