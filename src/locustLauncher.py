import gevent
import logging
import subprocess
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
    logging.warning('Setup ended')
    global env
    env = Environment()
    env.create_local_runner()
    env.create_web_ui('localhost', 8089)

    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    env.runner.start(1, 1)
    # env.runner.greenlet.join()
    # env.web_ui.greenlet.join()
    # subprocess.run(['locust'])


def clear():
    get_consumer().close()
    get_client().disconnect()


if __name__ == '__main__':
    try:
        main()
    except:
        clear()
