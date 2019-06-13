import random
import string

from locust import HttpLocust, TaskSet, task


def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class UserBehavior(TaskSet):
    userId = None
    groupId = None
    name = random_string()
    password = random_string()
    email = name + "@gmail.com"

    def on_start(self):
        self.create_user()
        self.create_group()

    def on_stop(self):
        self.delete_group()
        self.delete_user()

    def create_user(self):
        response = self.client.post("/users", {"name": self.name, "email": self.email, "password": self.password,
                                               "confirmPassword": self.password})
        self.userId = response.id

    def create_group(self):
        response = self.client.post("/groups", {"name": "group" + random_string(5), "owner": self.userId})
        self.groupId = response.id

    def delete_group(self):
        self.client.delete("/groups/" + self.groupId)

    def delete_user(self):
        self.client.delete("/users/" + self.userId)

    @task(1)
    def get_user(self):
        self.client.get("/users/" + self.userId)

    @task(1)
    def get_group(self):
        self.client.get("/groups/" + self.groupId)

    @task(1)
    def enter_group(self):
        self.client.put("/groups/" + self.groupId + "/add/" + self.userId)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
