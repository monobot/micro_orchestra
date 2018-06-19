#!/usr/bin/env python
import logging

import redis

logger = logging.getLogger()


class RedisSubscriber:
    HOST = 'localhost'
    PORT = 6379
    QUEUENAME = 'microservices'

    def __init__(self):
        self._redis = redis.StrictRedis(host=self.HOST, port=self.PORT)
        self.pub_sub = self._redis.pubsub()
        self.pub_sub.subscribe(self.QUEUENAME)

    def publish(self, message):
        self._redis.publish(self.QUEUENAME, message)

    def subscribe(self):
        message = self.pub_sub.get_message()
        if message:
            print(message)


if __name__ == '__main__':
    RedisSubscriber().subscribe()
