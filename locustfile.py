import uuid

from locust import HttpLocust, TaskSet, task


def random_string():
    return str(uuid.uuid4()).replace("-", "")


class UserBehavior(TaskSet):
    userId = None
    groupId = None

    def on_start(self):
        self.create_user()
        self.create_group()

    def on_stop(self):
        self.delete_group()
        self.delete_user()

    def create_user(self):
        name = random_string()
        email = name + "@gmail.com"
        password = random_string()
        response = self.client.post("/users", {"name": name, "email": email, "password": password,
                                               "confirmPassword": password})
        if not response.ok:
            print(str(response))
            raise ValueError("Could not create user")
        else:
            self.userId = response.text

    def create_group(self):
        response = self.client.post("/groups", {"name": "group" + random_string(), "owner": self.userId})
        if not response.ok:
            print(str(response))
            raise ValueError("Could not create group")
        else:
            self.groupId = response.text

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


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
