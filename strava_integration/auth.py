import time
import requests
import json

class StravaAuthenticator:
    def __init__(self, client_id: str, client_secret: str, token_file: str = "strava_tokens.json"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://www.strava.com/oauth/token"

    def _load_tokens(self) -> dict:
        try:
            with open(self.token_file, "r") as f:
                return json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Token file {self.token_file} not found")

    def _save_tokens(self, tokens_data: dict):
        with open(self.token_file, "w") as f:
            json.dump(tokens_data, f, indent=4)
    
    def get_access_token(self) -> str:
        tokens = self._load_tokens()

        if time.time() >= tokens.get("expires_at", 0) - 60:
            return self._refresh_token(tokens.get("refresh_token"))
        return tokens["access_token"]

    def _refresh_token(self, refresh_token: str) -> str:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        response = requests.post(self.token_url, data=payload)
        # raise an exception if the response is not successful
        reponse.raise_for_status()
        tokens = response.json()
        new_tokens = response.json()
        self._save_tokens(new_tokens)
        return new_tokens["access_token"]

