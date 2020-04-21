import time

import redis, os
from flask import Flask

app = Flask(__name__)

REDIS_HOST = os.getenv('REDIS_HOST')
if REDIS_HOST == None: REDIS_HOST = "redis" 

REDIS_PORT = os.getenv('REDIS_PORT')
if REDIS_PORT == None: REDIS_PORT = 6379

cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)