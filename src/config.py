import configparser
import os
from constant import CONFIG_FILE

# config file sections
RABBIT_MQ_SECTION = 'RABBITMQ'
TEST_SECTION = 'TEST'

configuration = None


class Config:
    def __init__(self):
        config = configparser.ConfigParser(interpolation=None)
        if not os.path.exists(CONFIG_FILE):
            raise FileNotFoundError('Cant find config file')
        config.read(CONFIG_FILE)

        self._rabbit_response_timeout = int(config[RABBIT_MQ_SECTION]['response_timeout'])
        self._rabbit_host = config[RABBIT_MQ_SECTION]['host']
        self._rabbit_port = int(config[RABBIT_MQ_SECTION]['port'])

        self._user_rate = float(config[TEST_SECTION]['user_rate'])
        self._max_users = int(config[TEST_SECTION]['max_users'])
        self._test_duration = int(config[TEST_SECTION]['test_duration']) \
            if int(config[TEST_SECTION]['test_duration']) and int(config[TEST_SECTION]['test_duration']) > 0 else None

    @property
    def rabbit_response_timeout(self):
        return self._rabbit_response_timeout

    @property
    def rabbit_host(self):
        return self._rabbit_host

    @property
    def rabbit_port(self):
        return self._rabbit_port

    @property
    def user_rate(self):
        return self._user_rate

    @property
    def max_users(self):
        return self._max_users

    @property
    def test_duration(self):
        return self._test_duration


def get_config() -> Config:
    global configuration
    if not configuration:
        configuration = Config()
    return configuration
