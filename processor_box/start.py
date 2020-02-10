import os
import uuid

from redis_connector import RedisConnector

HOST = 'redis_cache'
PORT = 6379
QUEUENAME = 'microservices'
QUEUES = [QUEUENAME, ]
MICRO_SERVICE_NAME = 'processor'

redis_connector_processor = RedisConnector(HOST, PORT, QUEUES, MICRO_SERVICE_NAME)

multiplier = int(os.environ.get('MULTIPLIER', '1'))


def process(message):
    first_operator = multiplier * message['data']['first']
    second_operator = message['data']['second']
    operation = message['data']['operation']
    if operation == '+':
        result = first_operator + second_operator
    redis_connector_processor.publish(
        'microservices',
        {
            "target": 'final',
            "message_id": str(uuid.uuid4()),
            "message": "calculated",
            "data": {
                'result': result
            },
        }
    )


while True:
    redis_connector_processor.subscribe(process)
