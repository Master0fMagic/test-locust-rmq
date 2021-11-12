from rabbitClient import get_client
from locust import User, task, events
from contracts import Error
from error import TimeoutException, ResponseException


class RmqUser(User):
    wait_time = 1

    @task
    def publish(self):
        get_client().send_for_response('random payload', on_response, on_timeout)


def on_response(response, completion_time):
    if response.Error == Error():
        print(f'Success response: {response}')
        events.request_success.fire(response_time=completion_time, response=response, request_type='amqp', name='amqp',
                                    response_length=0)
    else:
        print(f'Response with error: {response}')
        events.request_failure.fire(response_time=completion_time, response=response, request_type='amqp', name='amqp',
                                    response_length=0, exception=ResponseException())
    print(f'Response completed in {completion_time} ms')


def on_timeout(request_id):
    events.request_failure.fire(exception=TimeoutException(), response=None, request_type='amqp', name='amqp',
                                response_length=0)
    print(f'timeout for request: {request_id}')
