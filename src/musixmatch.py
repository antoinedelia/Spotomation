import os
import requests
from logger import Logger
from song import Song

MUSIXMATCH_API_KEY = os.getenv("MUSIXMATCH_API_KEY")


class Musixmatch:

    def __init__(self) -> None:
        self.client = None
        self.api_base_url = "https://api.musixmatch.com/ws/1.1/"
        self.logger = Logger("Musixmatch")

    def authenticate(self, api_key: str = MUSIXMATCH_API_KEY) -> bool:
        self.api_key = api_key
        self.logger.info("Successfully authenticated!")
        return True

    def _build_params(self, kwargs: dict = None) -> dict:
        kwargs["apikey"] = self.api_key
        return kwargs

    def get_song_id(self, song: Song) -> str:
        pass

    def get_lyrics_by_song_id(self, song_id: str) -> str:
        params = {
            "track_id": song_id,
        }
        response = requests.get(self.api_base_url + "track.lyrics.get", params=self._build_params(params))
        if response.status_code != 200:
            self.logger.warning(f"Failed to get lyrics for song_id: {song_id}")
            return None
        if (status_code := response.json()["message"]["header"]["status_code"]) != 200:
            self.logger.warning(f"Got an HTTP code {status_code} from Musixmatch for song_id: {song_id}")
            return None
        return response.json()["message"]["body"]["lyrics"]["lyrics_body"]
