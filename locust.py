# import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    def __init__(self, parent):
        super(QuickstartUser, self).__init__(parent)
        self.access = ""

    wait_time = between(1, 2)

    def on_start(self):
        # Send a POST request to login
        with self.client.post(
            "/auth/login/",
            {
                # Replace with appropriate credentials
                "username": "artist1",
                "password": "password123",
            },
        ) as response:
            try:
                # Parse JSON response
                json_response = response.json()
                if "access" in json_response:
                    self.access = json_response["access"]
                    print("Authorization: " f"Bearer {self.access}")
                else:
                    print("Login failed or 'access' key missing:", json_response)
            except Exception as e:
                print(
                    f"Error parsing response: {e}, Response content: {response.json()}"
                )

    @task
    def getAllAudios(self):
        if self.access:
            self.client.get(
                url="/api/audio",
                headers={"Authorization": f"Bearer {self.access}"},
            )
        else:
            print("Skipping API request because access token is missing.")
