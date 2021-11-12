import time
import logging
import pika
import threading
from abc import ABC, abstractmethod
from responseDto import AmqpResponse
from contracts import Response


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
        response = next(r for r in self._responses if r.is_expected_response(self._proto_response))
        if not response:
            return
        self._responses.remove(response)
        response.complete(response_data=self._proto_response)

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
        self._responses: list[AmqpResponse] = list()
        self._is_listening = False
        self._proto_response = proto_response

    def register_request(self, response: AmqpResponse):
        self._responses.append(response)

    def close(self):
        logging.warning('Closing consumer')
        if self._channel:
            self._channel.stop_consuming()
            self._channel.close()
        if self._connection:
            self._connection.close()
        if self._thread:
            self._thread.join(timeout=1)
        if self._expire_thread:
            self._expire_thread.join(timeout=1)

    def _check_expire(self):
        time.sleep(10)
        try:
            objects_to_delete = [r for r in self._responses if r.is_expired()]
            for obj_to_delete in objects_to_delete:
                self._responses.remove(obj_to_delete)
                obj_to_delete.complete_timeout()
        except RuntimeError as e:
            logging.error(f'Caught error: {e}')

    def __del__(self):
        self.close()


consumer = None


def get_consumer() -> BaseAmqpConsumer:
    """Singleton function for consumer"""
    global consumer
    if consumer is None:
        consumer = AmqpConsumer(Response())
    return consumer
