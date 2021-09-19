import requests
from dataclasses import dataclass
from logger import Logger
from models.song import Song


@dataclass
class MusicBrainz():
    api_base_url = "https://musicbrainz.org/ws/2/"
    covert_art_url = "https://coverartarchive.org/"
    logger = Logger("MusicBrainz")

    def authenticate(self):
        pass

    def find_song_id(self, song: Song) -> str:
        artists_as_string = " ".join(song.artists)
        query = f"{song.title} {artists_as_string}"
        params = {
            "fmt": "json",
            "query": query
        }
        self.logger.info(f"Looking for {query}")
        response = requests.get(self.api_base_url + "release", params=params)
        if response.status_code != 200:
            self.logger.error(f"MusicBrainz API returned {response.status_code}. Response: {response.json()}")
            return None

        releases = response.json()["releases"]

        if not releases:
            self.logger.warning(f"No release found for {song.title} - {song.artists}")
            return None

        # Try to find the most exact match
        artists_matches = self._filter_releases_by_artists(releases, song.artists)

        # If there is exactly one match, we return it
        if len(artists_matches) == 1:
            self.logger.info(f"Found exact match with artists: {song.artists}.")
            return artists_matches[0]["id"]

        self.logger.info(f"Found {len(artists_matches)} match(es) with artists. Trying to filter with the title")
        matches_to_filter = artists_matches or releases

        final_matches = self._filter_releases_by_title(matches_to_filter, song.title)

        if final_matches:
            return final_matches[0]["id"]
        else:
            return matches_to_filter[0]["id"]

    def _filter_releases_by_title(self, releases: list, title: str) -> list:
        return [release for release in releases if release["title"].upper() == title.upper()]

    def _filter_releases_by_artists(self, releases: list, artists: list) -> list:
        possible_releases = []
        for release in releases:
            artists_from_release = [artist["artist"]["name"] for artist in release["artist-credit"]]
            if set([artist.upper() for artist in artists_from_release]) == set([artist.upper() for artist in artists]):
                possible_releases.append(release)
        return possible_releases

    def _filter_releases_by_album(self, releases: list, album: str) -> list:
        return [release for release in releases if release["release-group"]["title"].upper() == album.upper()]

    def get_metadata_by_song_id(self, id: str) -> dict:
        params = {
            "inc": "artist-credits+release-groups+genres",
            "fmt": "json",
        }
        response = requests.get(self.api_base_url + "release/" + id, params=params)
        if response.status_code != 200:
            self.logger.error(f"MusicBrainz API returned {response.status_code}. Response: {response.json()}")
            return None

        data = {
            "artists": [credited["artist"]["name"] for credited in response.json()["artist-credit"]],
            "title": response.json()["title"],
            "album": response.json()["release-group"]["title"],
            "release_date": response.json().get("date"),
            "genres": response.json().get("genres")
        }

        return data

    def get_cover_art_url_by_id(self, id: str) -> str:
        try:
            response = requests.get(self.covert_art_url + "release/" + id, timeout=5)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
            self.logger.warning(f"Timeout for release {id}")
            return None

        if response.status_code == 404:
            self.logger.warning(f"Cover art not found for release {id}")
            return None
        if response.status_code != 200:
            self.logger.error(f"Cover Art Archive API returned {response.status_code}. Response: {response.text}")
            return None

        return response.json()["images"][0]["thumbnails"]["large"]
