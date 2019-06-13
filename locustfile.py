from locust import HttpLocust, TaskSet, task
import string, random

class UserBehavior(TaskSet):

    def randomString(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    userId = None
    groupId = None
    name = randomString()
    password = randomString()
    email = name + "@gmail.com"

    def on_start(self):
        self.createUser()
        self.createGroup()

    def on_stop(self):
        self.deleteGroup()
        self.deleteUser()

    def createUser(self):
        response = self.client.post("/user", {"name": self.name, "email": self.email, "password": self.password, "confirmPassword": self.password})
        self.userId = response.id

    def createGroup(self):
        self.client.post("/groups", {"name": "group" + self.randomString(5), "owner": self.userId})
        self.groupId = response.id

    def deleteGroup(self):
        self.client.delete("/groups/" + self.groupId)

    def deleteUser(self):
        self.client.delete("/users/" + self.userId)

    @task(1)
    def getUser(self):
        self.client.get("/users/" + self.userId)

    @task(1)
    def getGroup(self):
        self.client.get("/groups/" + self.groupId)

    @task(1)
    def enterGroup(self):
        self.client.put("/groups/" + self.groupId + "/add/" + self.userId)    


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
