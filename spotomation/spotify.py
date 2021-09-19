import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from logger import Logger


class Spotify:
    def __init__(self) -> None:
        self.client: spotipy.Spotify = None
        self.logger = Logger("Spotify")

    def authenticate_oauth(self) -> bool:
        """
        Authenticate to Spotify
        :return: None
        """
        self.client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self.logger.info("Successfully authenticated!")
        return True

    def get_playlist_tracks_by_uri(self, uri: str) -> list:
        """
        Get playlist by uri
        :param uri: playlist uri
        :return: playlist
        """
        playlist_id = uri.split("/")[-1]
        if "?" in playlist_id:
            playlist_id = playlist_id.split("?")[0]

        tracks = []
        results = self.client.playlist_items(playlist_id=playlist_id)
        while results["next"]:
            for item in results["items"]:
                tracks.append(item["track"])
            results = self.client.next(results)

        # We do an extra for loop to get the last tracks
        for item in results["items"]:
            tracks.append(item["track"])
        return tracks
