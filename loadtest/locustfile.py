import json

from random import choice

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)


HOST =  "http://localhost:8000"
VOTING = 2
VOTING_YESNO = 4


class DefVisualizer(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/{0}/".format(VOTING))


class DefVisualizerYesNo(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/yesno/{0}/".format(VOTING_YESNO))

class VotingStatsTaskSet(TaskSet):
    @task
    def get_voting_stats(self):
        voting_id = 2
        self.client.get(f"/{voting_id}/stats")

class AdminVotingStats(TaskSet):
    @task
    def get_admin_voting_stats(self):
        self.client.get("/admin/voting/stats")

class AdminVoting(TaskSet):
    @task
    def get_admin_voting(self):
        self.client.get("/admin/voting")
        
class AdminQuestion(TaskSet):
    @task
    def get_admin_question(self):
        self.client.get("/admin/question")

class AdminUser(TaskSet):
    @task
    def get_admin_user(self):
        self.client.get("/admin/user")

class AdminUserData(TaskSet):
    @task
    def get_admin_user_data(self):
        self.client.get("/admin/userdata")

class AdminAuthToken(TaskSet):
    @task
    def get_admin_auth_token(self):
        self.client.get("/admin/authtoken")


class GraficaStatsTaskSet(TaskSet):
    @task
    def get_grafica_stats(self):
        self.client.get(f"/admin/grafica")


class DefVoters(SequentialTaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    @task
    def voting(self):
        headers = {
            'Authorization': 'Token ' + self.token.get('token'),
            'content-type': 'application/json'
        }
        self.client.post("/store/", json.dumps({
            "token": self.token.get('token'),
            "vote": {
                "a": "12",
                "b": "64"
            },
            "voter": self.usr.get('id'),
            "voting": VOTING
        }), headers=headers)


    def on_quit(self):
        self.voter = None

class DefVotersYesNo(SequentialTaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    @task
    def voting(self):
        headers = {
            'Authorization': 'Token ' + self.token.get('token'),
            'content-type': 'application/json'
        }
        self.client.post("/custom/store/yesno/", json.dumps({
            "token": self.token.get('token'),
            "vote": {
                "a": "12",
                "b": "64"
            },
            "voter": self.usr.get('id'),
            "voting": VOTING_YESNO
        }), headers=headers)


    def on_quit(self):
        self.voter = None

class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)

class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time= between(3,5)


class VisualizerYesNo(HttpUser):
    host = HOST
    tasks = [DefVisualizerYesNo]
    wait_time = between(3,5)

class VotersYesNo(HttpUser):
    host = HOST
    tasks = [DefVotersYesNo]
    wait_time= between(3,5)


class StatsFrontend(HttpUser):
    host = 'http://localhost:5173'
    tasks = [VotingStatsTaskSet]
    wait_time = between(3, 5)

class StatsBackend(HttpUser):
    host = HOST
    tasks = [VotingStatsTaskSet]
    wait_time = between(3, 5)

class AdminVotingStatsFrontend(HttpUser):
    host = 'http://localhost:5173'
    tasks = [AdminVotingStats]
    wait_time = between(3, 5)


class StatsGrafica(HttpUser):
    host = 'http://localhost:5173'
    tasks = [GraficaStatsTaskSet]
    wait_time = between(3, 5)

class AdminVotingFrontend(HttpUser):
    host = 'http://localhost:5173'
    tasks = [AdminVoting]
    wait_time = between(3, 5)

class AdminQuestionFrontend(HttpUser):
    host = 'http://localhost:5173'
    tasks = [AdminQuestion]
    wait_time = between(3, 5)

class AdminUserFrontend(HttpUser):
    host = 'http://localhost:5173'
    tasks = [AdminUser]
    wait_time = between(3, 5)

class AdminUserDataFrontend(HttpUser):
    host = 'http://localhost:5173'
    tasks = [AdminUserData]
    wait_time = between(3, 5)
    
class AdminAuthTokenFrontend(HttpUser):
    host = 'http://localhost:5173'
    tasks = [AdminAuthToken]
    wait_time = between(3, 5)