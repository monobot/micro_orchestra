import os
import uuid
from time import sleep

from redis_connector import RedisConnector

HOST = 'redis_cache'
PORT = 6379
QUEUENAME = 'microservices'
QUEUES = [QUEUENAME, ]
MICRO_SERVICE_NAME = 'publisher'
start_number = int(os.environ.get('START_NUMBER', 1))
operation = int(os.environ.get('OPERATION', '+'))

redis_connector_publisher = RedisConnector(HOST, PORT, QUEUES, MICRO_SERVICE_NAME)

while True:
    processor_instances = redis_connector_publisher.publish('ping:processor', {"message": "ping"})
    final_instances = redis_connector_publisher.publish('ping:final', {"message": "ping"})
    publisher_instances = redis_connector_publisher.publish('ping:publisher', {"message": "ping"})
    message = {
        "data": {
            'first': start_number,
            'operation': operation,
            'second': start_number,
        },
        'final_instances': final_instances,
        'processor_instances': processor_instances,
        'publisher_instances': publisher_instances,
        "message_id": str(uuid.uuid4()),
        "message": "Bingo {}".format(start_number),
        "target": 'processor',
    }
    redis_connector_publisher.publish(QUEUENAME, message)
    start_number += 1
