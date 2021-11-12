import logging
import time

from contracts import Error

from rabbitClient import get_client
from rabbitConsumer import get_consumer
from random import random


def setup():
    logging.basicConfig(format='%(levelname) -s at %(asctime) -s: %(message)s', level=logging.INFO)
    get_client()
    consumer = get_consumer()
    consumer.start_listening(rk='r.response', queue='q.response.test', exchange='e.general')


def clear():
    get_consumer().close()
    get_client().disconnect()


def main():
    setup()

    rmq_client = get_client()
    for _ in range(10):
        rmq_client.send_for_response(f'Hello world, {random()} try',
                                     on_response, on_timeout)
        time.sleep(4)


def on_response(response, completion_time):
    if response.Error == Error():
        logging.info(f'Success response: {response}')
    else:
        logging.info(f'Response with error: {response}')
    logging.info(f'Response completed in {completion_time} ms')


def on_timeout(request_id):
    logging.info(f'timeout for request: {request_id}')


if __name__ == '__main__':
    main()
