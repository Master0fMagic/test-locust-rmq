# import configs for timeout
import time


class AmqpResponse:
    """on_response_callback - function(response_object, completion_time: int),
    on_timeout_callback - function(request_idL str),
    send_at - timestamp (millis) where request was send,
    response - proto object for parsing body,
    check_function - function(response) -> bool: uses for check if caught message is expected for response"""

    def __init__(self, request_id: str, on_response_callback, on_timeout_callback, send_at: int, check_function=None):
        self._request_id = request_id
        self._on_response_callback = on_response_callback
        self._on_timeout_callback = on_timeout_callback
        self._send_at = send_at
        self._expire_at = send_at + 120_000
        if check_function:
            self._check_function = check_function
        else:
            self._check_function = lambda response: response.id == self._request_id

    def complete(self, response_data) -> None:
        now = int(time.time() * 1000)

        if self._expire_at <= now:
            self._on_timeout_callback(self._request_id)
            return

        completion_time = now - self._send_at
        self._on_response_callback(response_data, completion_time)

    def complete_timeout(self) -> None:
        self._on_timeout_callback(self._request_id)

    def is_expired(self) -> bool:
        return int(time.time() * 1000) >= self._expire_at

    def is_expected_response(self, response) -> bool:
        return self._check_function(response)
