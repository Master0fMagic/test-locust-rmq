from locust.env import Environment
from locustfile import RmqUser
from rabbitClient import get_client
from rabbitConsumer import get_consumer


def setup():
    get_client()
    consumer = get_consumer()
    consumer.start_listening(rk='r.response', queue='q.response.test', exchange='e.general')


def clear():
    get_consumer().close()
    get_client().disconnect()


def main():
    setup()
    env = Environment(user_classes=[RmqUser])
    env.create_local_runner()
    env.create_web_ui('localhost', 8089)
    env.web_ui.greenlet.join()
    env.runner.start(1, 1)


def clear():
    get_consumer().close()
    get_client().disconnect()


if __name__ == '__main__':
    try:
        main()
    finally:
        clear()
