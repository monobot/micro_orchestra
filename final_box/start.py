#!/usr/bin/env python
from redis_connector import RedisConnector


def process(message):
    print(message)


HOST = 'redis_cache'
PORT = 6379
QUEUENAME = 'microservices'
QUEUES = [QUEUENAME, ]
MICRO_SERVICE_NAME = 'final'

redis_connector_final = RedisConnector(HOST, PORT, QUEUES, MICRO_SERVICE_NAME)
while True:
    redis_connector_final.subscribe(process)
