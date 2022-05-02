from random import choice

from locust import HttpUser, constant_pacing, task


class User(HttpUser):
    host = "http://localhost:8000"
    wait_time = constant_pacing(1 / 10)

    @task
    def vote(self):
        participant_id = choice([1, 2, 3])

        self.client.get(f"/vote/{participant_id}")
