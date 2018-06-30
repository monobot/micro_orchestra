#!/usr/bin/env python
import json
import redis
import time
import uuid


class RedisConnector:

    def __init__(self, host, port, queues, service_name):
        """Init method for RedisConnector

        :param host: the redis host yu will connect to.
        :type host: str

        :param port: redis port.
        :type port: int

        :param queues: the name of the redis queue you need to subscribe to.
        :type queues: string

        :param service_name: The name of the service is connecting to the queue.
        :type service_name: type

        :rtype: None
        """
        self._redis = redis.StrictRedis(host=host, port=port)
        self.pub_sub = self._redis.pubsub()
        self.pub_sub.subscribe(queues)
        self.service_name = service_name

    def __enter__(self):
        """Implement with statement."""
        return self

    def __exit__(self, *args, **kwargs):
        """Implement with statement."""
        return self.close()

    def close(self):
        self.pub_sub.close()

    def publish(self, message):
        """Will publish the message to the queue you are subscribed to.

        :param message: message you want to publish.
        :type message: str

        :rtype: None
        """
        self._redis.publish(self.queue_name, message)

    def subscribe(self):
        """Subscribes to the redis queue.

        :rtype: None
        """
        message = self.pub_sub.get_message()
        if message:
            data = message['data']
            if message['type'] == 'message':
                data = json.loads(data.decode('utf8').replace("'", '"'))
                # No target means promiscuous mode for that message, no lock will be used
                if data.pop('target') is None:
                    self._process(data)
                elif data.pop('target') == self.service_name:
                    if self._acquire_lock(data['message_id']):
                        self._process(data)

    def _acquire_lock(self, message_id, lock_timeout=10):
        """Will lock the redis key for a max of 10 seconds,
        if the lock is free then it will process the message inmediatly, leaving it locked for the lock_timeout in all
        the cases, thus not allowing to process the messege to any other service.

        :rtype: bool
        """
        expire_time = time.time() + (lock_timeout / 2)
        while time.time() < expire_time:
            if self._redis.setnx(message_id, expire_time):
                self._redis.expire(message_id, lock_timeout)
                return True

            elif not self._redis.ttl(message_id):
                self._redis.expire(message_id, lock_timeout)

            time.sleep(0.001)
        return False

    def _process(self, message):
        first_operator = message['data']['first']
        second_operator = message['data']['second']
        operation = message['data']['operation']
        print('processing {}'.format(message))
        if operation == '+':
            result = first_operator + second_operator
        self.publish(
            json.dumps(
                {
                    "target": 'final',
                    "message_id": str(uuid.uuid4()),
                    "message": "calculated",
                    "data": {
                        'result': result
                    }
                }
            )
        )


HOST = 'redis_cache'
PORT = 6379
QUEUENAME = 'microservices'
MICRO_SERVICE_NAME = 'processor'

redis_subscriber = RedisConnector(HOST, PORT, QUEUENAME, MICRO_SERVICE_NAME)
while True:
    redis_subscriber.subscribe()
