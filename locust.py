from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

    @task(1)
    def lol_index(self):
        self.client.get("/lol")

    @task(1)
    def team_profile(self):
        self.client.get("/lol/teams/420")
    
    @task(1)
    def tournament(self):
        self.client.get("/lol/tournaments/10")

    @task(1)
    def university(self):
        self.client.get("/lol/universities/1553")

    @task(1)
    def university_index(self):
        self.client.get("/lol/universities")

    @task(1)
    def user_profile(self):
        self.client.get("/lol/users/666")
    
    @task(1)
    def scrims(self):
        self.client.get("/lol/scrims")

    @task(1)
    def schedule(self):
        self.client.get("/lol/schedules")

    @task(1)
    def playoffs(self):
        self.client.get("/lol/playoffs")

    @task(1)
    def standings(self):
        self.client.get("/lol/standings")
    
    @task(1)
    def tournament(self):
        self.client.get("/lol/tournaments/10")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 2000
