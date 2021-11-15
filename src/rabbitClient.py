import logging
import time
import uuid
import constant

import pika

from contracts import Request
from responseDto import AmqpResponse
from rabbitConsumer import get_consumer
from config import get_config


class RabbitMQClient(object):
    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=get_config().rabbit_host,
                                                                             port=get_config().rabbit_port))
        self._channel = self._connection.channel()

    def send_for_response(self, payload, on_response_call_back, on_timeout_call_back):
        request = Request()
        request.id = str(uuid.uuid4())
        request.payload = payload

        response_dto = AmqpResponse(request_id=request.id, on_response_callback=on_response_call_back,
                                    on_timeout_callback=on_timeout_call_back, send_at=int(time.time() * 1000),
                                    timeout=get_config().rabbit_response_timeout)

        consumer = get_consumer()
        consumer.start_listening(rk=constant.RESPONSE_ROUTING_KEY, queue=constant.RESPONSE_QUEUE,
                                 exchange=constant.EXCHANGE)
        consumer.register_request(response_dto)

        logging.info(f'Sending request: {request}')
        self._channel.basic_publish(exchange=constant.EXCHANGE, routing_key=constant.REQUEST_ROUTING_KEY,
                                    body=request.SerializeToString())

    def disconnect(self):
        logging.warning('Disconnecting rmq client')
        if self._channel is not None:
            self._channel.close()
        if self._connection is not None:
            self._connection.close()

    def __del__(self):
        self.disconnect()


client = None


def get_client():
    global client
    if client is None:
        client = RabbitMQClient()
    return client
