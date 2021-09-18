import os
import requests
from logger import Logger
from song import Song

GENIUS_CLIENT_ID = os.getenv("GENIUS_CLIENT_ID")
GENIUS_CLIENT_SECRET = os.getenv("GENIUS_CLIENT_SECRET")


class Genius:

    def __init__(self) -> None:
        self.client = None
        self.token_url = "https://api.genius.com/oauth/token"
        self.api_base_url = "https://api.genius.com/"
        self.logger = Logger("Genius")

    def authenticate_oauth(self, client_id: str = GENIUS_CLIENT_ID, client_secret: str = GENIUS_CLIENT_SECRET) -> bool:
        self.client_id = client_id
        self.client_secret = client_secret

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "response_type": "token",
            "grant_type": "client_credentials"
        }

        response = requests.post(self.token_url, json=data)
        self.access_token = response.json()["access_token"]
        self.logger.info("Successfully authenticated!")
        return True

    def _build_headers(self):
        return {
            "Authorization": "Bearer " + self.access_token
        }

    def get_song_id(self, song: Song) -> str:
        pass

    def get_lyrics_for_song(self, song: Song) -> str:
        response = requests.get(self.api_base_url + f"songs/{song.song_id}", headers=self._build_headers())
        return response.json()["response"]["lyrics_body"]
