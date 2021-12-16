from locust import HttpLocust, TaskSet, task, between
import random
import datetime
import string


class UserTaskSet(TaskSet):
    def on_start(self):
        self.client.headers = {'Content-Type': 'application/json;'}

    @task(1)
    def fetch_user(self):
        self.client.get("/users")

    @task(2)
    def create_user(self):
        gDate =str(datetime.datetime.now())
        username = ''.join(random.choices(string.ascii_letters, k=10))
        password = ''.join(random.choices(string.ascii_letters, k=10))
        first_name = ''.join(random.choices(string.ascii_letters, k=10))
        last_name = ''.join(random.choices(string.ascii_letters, k=10))
        gender = "M"
        create_at = gDate
        status = "1"
        self.client.post("/users?username={}&password={}&first_name={}&last_name={}&password={}&gender={}&create_at={}&status={}".format(username, password, first_name, last_name, gender, create_at, status))


class UserLocust(HttpLocust):
    task_set = UserTaskSet

    wait_time = between(0.100, 1.500)