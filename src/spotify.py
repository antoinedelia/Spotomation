import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Spotify:
    def __init__(self, scopes: str = 'user-library-read') -> None:
        self.client: spotipy.Spotify = None
        self.scopes = scopes

    def authenticate_oauth(self) -> None:
        """
        Authenticate to Spotify
        :return: None
        """
        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scopes))
        print("Successfully authenticated!")

    def get_playlist_tracks_by_uri(self, uri: str) -> list:
        """
        Get playlist by uri
        :param uri: playlist uri
        :return: playlist
        """
        playlist_id = uri.split('/')[-1]
        if "?" in playlist_id:
            playlist_id = playlist_id.split('?')[0]

        tracks = []
        results = self.client.playlist_items(playlist_id=playlist_id)
        while results['next']:
            for item in results['items']:
                tracks.append(item['track'])
            results = self.client.next(results)

        # We do an extra for loop to get the last tracks
        for item in results['items']:
            tracks.append(item['track'])
        return tracks
