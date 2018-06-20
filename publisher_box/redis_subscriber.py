#!/usr/bin/env python
import json
import redis

MICRO_SERVICE_NAME = 'publisher'


class RedisSubscriber:
    HOST = 'redis_cache'
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
            data = message['data']
            if not isinstance(data, int):
                data = json.loads(data.decode('utf8').replace("'", '"'))
                data.pop('target')
                print(data)


if __name__ == '__main__':
    redis_subscriber = RedisSubscriber()
    t = 1
    while True:
        redis_subscriber.publish(
            json.dumps(
                {
                    "target": "subscriber",
                    "message": "Connection working {}".format(t),
                    "data": {}
                }
            )
        )
        t += 1
