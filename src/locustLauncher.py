import gevent
import logging
import constant
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust import events
from locustfile import RmqUser
from rabbitClient import get_client
from rabbitConsumer import get_consumer
from config import get_config

env: Environment = None


def setup():
    logging.basicConfig(format='%(levelname) -s at %(asctime) -s: %(message)s', level=logging.INFO)
    get_client()
    consumer = get_consumer()
    consumer.start_listening(rk=constant.RESPONSE_ROUTING_KEY, queue=constant.RESPONSE_QUEUE,
                             exchange=constant.EXCHANGE)


def clear():
    get_consumer().close()
    get_client().disconnect()


def main():
    setup()
    logging.warning('Setup ended')
    global env
    env = Environment(user_classes=[RmqUser], events=events)
    env.create_local_runner()
    env.create_web_ui('localhost', 8089)

    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    env.runner.start(user_count=get_config().max_users, spawn_rate=get_config().user_rate)

    if get_config().test_duration:
        gevent.spawn_later(get_config().test_duration, lambda: env.runner.quit())

    env.runner.greenlet.join()
    env.web_ui.stop()


if __name__ == '__main__':
    try:
        main()
    except:
        clear()
