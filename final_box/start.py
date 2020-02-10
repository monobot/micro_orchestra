import os

from redis_connector import RedisConnector

field_name = os.environ.get('FIELD_NAME', 'default_fieldname')


def process(message):
    print(f'{field_name}: {message}')


HOST = 'redis_cache'
PORT = 6379
QUEUENAME = 'microservices'
QUEUES = [QUEUENAME, ]
MICRO_SERVICE_NAME = 'final'

redis_connector_final = RedisConnector(HOST, PORT, QUEUES, MICRO_SERVICE_NAME)
while True:
    redis_connector_final.subscribe(process)
