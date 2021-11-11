import time
from abc import ABC, abstractmethod
from src.responseDto import AmqpResponse
from contracts import Response

import pika
import threading


class BaseAmqpConsumer(ABC):
    @abstractmethod
    def register_request(self, response: AmqpResponse):
        pass

    @abstractmethod
    def start_listening(self, rk: str, queue: str, exchange: str):
        pass

    @abstractmethod
    def _callback(self, channel, method, properties, body):
        pass

    @abstractmethod
    def close(self):
        pass


class AmqpConsumer(BaseAmqpConsumer):
    def _callback(self, channel, method, properties, body):
        self._proto_response.ParseFromString(body)
        # add message logging
        if self._proto_response.id not in self._response_dict:
            return
        amqp_response: AmqpResponse = self._response_dict.pop(self._proto_response.id)
        amqp_response.complete(response_data=self._proto_response)

    def start_listening(self, rk: str, queue: str, exchange: str):
        if self._is_listening:
            return

        self._thread = threading.Thread(target=self._start, args=[rk, queue, exchange])
        # self._thread.daemon = True
        self._thread.start()

        self._expire_thread = threading.Thread(target=self._check_expire())
        # self._expire_thread.daemon = True
        self._expire_thread.start()

        self._is_listening = True

    def _start(self, rk: str, queue: str, exchange: str):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.108',
                                                                             port=5672))
        self._channel = self._connection.channel()

        self._channel.queue_declare(queue, auto_delete=True)
        self._channel.queue_bind(queue, exchange, rk)

        self._channel.basic_consume(queue, self._callback, True)

        self._channel.start_consuming()

    def __init__(self, proto_response):
        self._response_dict = dict()
        self._is_listening = False
        self._proto_response = proto_response

    def register_request(self, response: AmqpResponse):
        if response.request_id in self._response_dict:
            return

        self._response_dict[response.request_id] = response

    def close(self):
        self._channel.stop_consuming()
        self._channel.close()
        self._connection.close()
        self._thread.join(timeout=1)
        self._expire_thread.join(timeout=1)

    def _check_expire(self):
        time.sleep(10)
        keys_to_delete = []
        try:
            for key in self._response_dict.keys():
                response: AmqpResponse = self._response_dict.get(key)
                if response.expire_at <= datetime.datetime.now().second * 1000:
                    keys_to_delete.append(response)
        except RuntimeError as e:
            pass
            # todo add logging

        for key in keys_to_delete:
            response: AmqpResponse = self._response_dict.pop(key)
            response.complete_timeout()


consumer = None


def get_consumer() -> BaseAmqpConsumer:
    """Singleton function for consumer"""
    global consumer
    if consumer is None:
        consumer = AmqpConsumer(Response())
    return consumer
