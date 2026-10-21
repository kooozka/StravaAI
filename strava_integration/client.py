import requests

class StraaClient:
    def __init__(self, access_token: str):
        self.base_url = "https://www.strava.com/api/v3"
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_activitiees(self, per_page: int = 30, page: int = 1) -> list:
        url = f"{self.base_url}/athlete/activities"
        params = {
            "per_page": per_page,
            "page": page
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()