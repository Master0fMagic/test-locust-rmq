from contracts import Error

from rabbitClient import get_client
from random import random


def main():
    client = get_client()
    for _ in range(10):
        client.send_for_response(f'Hello world, {random()} try',
                                 on_response, on_timeout)


def on_response(response, completion_time):
    if response.Error and response.Error != Error:
        print(f'Success response: {response}')
    else:
        print(f'Response with error: {response}')
    print(f'Response completed in {completion_time} ms')


def on_timeout(request_id):
    print(f'timeout for request: {request_id}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        client = get_client()
        client.disconnect()
