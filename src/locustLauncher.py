import gevent
import logging
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locustfile import RmqUser
from rabbitClient import get_client
from rabbitConsumer import get_consumer

env: Environment = None


def setup():
    logging.basicConfig(format='%(levelname) -s at %(asctime) -s: %(message)s', level=logging.INFO)
    get_client()
    consumer = get_consumer()
    consumer.start_listening(rk='r.response', queue='q.response.test', exchange='e.general')


def clear():
    get_consumer().close()
    get_client().disconnect()

    # global env
    # env.runner.greenlet.join()
    # env.web_ui.stop()


def main():
    setup()
    global env
    env = Environment(user_classes=[RmqUser])
    env.create_local_runner()
    env.create_web_ui('localhost', 8089)

    # gevent.spawn(stats_printer(env.stats))
    # gevent.spawn(stats_history, env.runner)

    env.runner.start(1, 1)


def clear():
    get_consumer().close()
    get_client().disconnect()


if __name__ == '__main__':
    try:
        main()
    finally:
        clear()
