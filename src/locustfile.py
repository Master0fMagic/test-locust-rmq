from rabbitClient import get_client

from locust import User, task
import time


class MyLocust(User):
    min_wait = 1000
    max_wait = 1000

    @task
    def publish(self):
        get_client().publish()
        time.sleep(1)
