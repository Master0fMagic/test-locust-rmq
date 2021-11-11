import time
import uuid

import pika

from contracts import Request
from responseDto import AmqpResponse
from rabbitConsumer import get_consumer


class RabbitMQClient(object):
    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.108',
                                                                             port=5672))
        self._channel = self._connection.channel()

    def send_for_response(self, payload, on_response_call_back, on_timeout_call_back):
        request = Request()
        request.id = str(uuid.uuid4())
        request.payload = payload

        response_dto = AmqpResponse(request.id, on_response_call_back, on_timeout_call_back,
                                    int(time.time() * 1000))

        consumer = get_consumer()
        consumer.start_listening(rk='r.response', queue='q.response.test', exchange='e.general')
        consumer.register_request(response_dto)

        print(f'Sending request: {request}')
        self._channel.basic_publish(exchange='e.general', routing_key='r.request.test',
                                    body=request.SerializeToString())

    def disconnect(self):
        if self._channel is not None:
            self._channel.close()
        if self._connection is not None:
            self._connection.close()
        get_consumer().close()


client = None


def get_client():
    global client
    if client is None:
        client = RabbitMQClient()
    return client
