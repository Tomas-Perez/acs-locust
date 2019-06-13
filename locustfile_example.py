from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    @task(2)
    def index(self):
        self.client.get("/")

    @task
    def profile(self):
        self.client.get("/profile")

    def on_start(self):
        self.client.post("/login", {"username": "ellen_key", "password": "education"})

    def on_stop(self):
        self.client.post("/logout", {"username": "ellen_key", "password": "education"})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
