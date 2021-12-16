from locust import HttpLocust, TaskSet, task
from locust import ResponseError
import json
  
   
class UserBehavior(TaskSet):
   
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.token = ""
        self.headers = {}
   
    @task(1)
    def lol_index(self):
        self.client.get("/")
   
    @task(1)
    def get_users(self):
        self.client.get("/users")    

          
        return json.loads(response._content)['access']
   
   
  
class WebsiteUser(HttpLocust):
    # The task_set attribute should point
    # to a TaskSet class which defines 
    # the behaviour of the user
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000