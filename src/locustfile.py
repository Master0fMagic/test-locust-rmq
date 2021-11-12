import logging

from rabbitClient import get_client
from locust import User, task, events, constant
from contracts import Error
from error import TimeoutException, ResponseException

REQUEST_TYPE = 'AMQP'


class RmqUser(User):
    wait_time = constant(1)

    @task
    def publish(self):
        get_client().send_for_response('random payload', on_response, on_timeout)


def on_response(response, completion_time):
    if response.Error == Error():
        logging.info(f'Success response: {response}')
        # events.request_success.fire(response_time=completion_time, request_type='amqp', name='amqp', response_length=0)
        fire_success(completion_time, response)
    else:
        logging.info(f'Response with error: {response}')
        # events.request_failure.fire(response_time=completion_time, request_type='amqp', name='amqp', response_length=0,
        #                             exception=ResponseException())
        fire_error(completion_time, response, ResponseException())
    logging.info(f'Response completed in {completion_time} ms')


def on_timeout(request_id):
    # events.request_failure.fire(exception=TimeoutException(), request_type='amqp', name='amqp', response_length=0,
    #                             response_time=0)
    fire_error(0, None, TimeoutException())
    logging.info(f'timeout for request: {request_id}')


def fire_success(completion_time, response):
    events.request.fire(request_type=REQUEST_TYPE, name='Local docker RabbitMQ instance', response_time=completion_time,
                        response_length=0, response=response, context=None, exception=None)


def fire_error(completion_time, response, exception: BaseException):
    events.request.fire(request_type=REQUEST_TYPE, name='Local docker RabbitMQ instance', response_time=completion_time,
                        response_length=0, response=response, context=None, exception=BaseException)
