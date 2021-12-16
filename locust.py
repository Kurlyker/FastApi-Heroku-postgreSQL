from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):

    @task(1)
    def lol_index(self):
        self.client.get("/")
   
    @task(1)
    def lol_index(self):
        self.client.get("/users")        

  

class WebsiteUser(HttpUser):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 2000
