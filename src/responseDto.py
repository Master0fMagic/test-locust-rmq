# import configs for timeout
import time


class AmqpResponse:
    """on_response_callback - function(response_object, completion_time: int),
    on_timeout_callback - function(request_idL str),
    send_at - timestamp (millis) where request was send,
    response - proto object for parsing body"""

    def __init__(self, request_id: str, on_response_callback, on_timeout_callback, send_at: int):
        self._request_id = request_id
        self._on_response_callback = on_response_callback
        self._on_timeout_callback = on_timeout_callback
        self._send_at = send_at
        self._expire_at = send_at + 120_000

    @property
    def request_id(self):
        return self._request_id

    @property
    def expire_at(self):
        return self._expire_at

    def complete(self, response_data):
        now = int(time.time() * 1000)

        if self._expire_at <= now:
            self._on_timeout_callback(self._request_id)
            return

        completion_time = now - self._send_at
        self._on_response_callback(response_data, completion_time)

    def complete_timeout(self):
        self._on_timeout_callback(self._request_id)
