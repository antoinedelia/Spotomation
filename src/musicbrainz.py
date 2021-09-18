import requests
from dataclasses import dataclass
from logger import Logger


@dataclass
class MusicBrainz():
    api_base_url = "https://musicbrainz.org/ws/2/"
    covert_art_url = "https://coverartarchive.org/"
    logger = Logger("MusicBrainz")

    def authenticate(self):
        pass

    def find_song_id(self, title: str = None, artists: list = [], album: str = None) -> str:
        artists_as_string = " ".join(artists)
        query = f"{title} {artists_as_string} {album}"
        params = {
            "fmt": "json",
            "query": query
        }
        self.logger.info(f"Looking for {query}")
        response = requests.get(self.api_base_url + "release", params=params)
        if response.status_code != 200:
            self.logger.error(f"MusicBrainz API returned {response.status_code}. Response: {response.json()}")

        releases = response.json()["releases"]

        if len(releases) == 0:
            self.logger.warning(f"No release found for {title} - {artists} - {album}")
            return None

        # Try to find the most exact match
        exact_matches = self._filter_releases_by_artists(releases, artists)

        # If there is exactly one match, we return it
        if len(exact_matches) == 1:
            self.logger.info(f"Found exact match with artists: {artists}.")
            return exact_matches[0]["id"]

        # If there is no exact match for the title, we try to look with the title, then the album
        if len(exact_matches) == 0:
            self.logger.debug(f"No exact match found for artists: {artists}.")
            exact_matches = self._filter_releases_by_title(releases, title)
            if len(exact_matches) == 0:
                self.logger.debug(f"No exact match found for title: {title}.")
                exact_matches = self._filter_releases_by_album(releases, album)
                if len(exact_matches) == 0:
                    self.logger.debug(f"No exact match found for album: {album}.")
                    return None

        # If there are multiple matches, we try to filter with the title or the album
        # This is very messy, should think of a better way to do it
        if len(exact_matches) > 1:
            self.logger.info(f"Multiple matches ({len(exact_matches)}) found.")
            new_exact_matches = self._filter_releases_by_title(exact_matches, title)
            if len(new_exact_matches) == 1:
                self.logger.info(f"Found exact match with title {title} and artists {artists}.")
                return new_exact_matches[0]["id"]
            if len(new_exact_matches) == 0:
                final_exact_matches = self._filter_releases_by_album(exact_matches, album)
                if len(final_exact_matches) >= 1:
                    self.logger.info(f"Found multiple matches {(len(final_exact_matches))} even with album.")
                    return final_exact_matches[0]["id"]
                if len(final_exact_matches) == 0:
                    return exact_matches[0]["id"]
            if len(new_exact_matches) > 1:
                self.logger.info(f"Found multiple matches ({len(new_exact_matches)}) with title.")
                final_exact_matches = self._filter_releases_by_album(new_exact_matches, album)
                if len(final_exact_matches) >= 1:
                    return final_exact_matches[0]["id"]
                if len(final_exact_matches) == 0:
                    return new_exact_matches[0]["id"]

    def _filter_releases_by_title(self, releases: list, title: str) -> list:
        return [release for release in releases if release["title"].upper() == title.upper()]

    def _filter_releases_by_artists(self, releases: list, artists: list) -> list:
        possible_releases = []
        for release in releases:
            artists_from_release = [artist["artist"]["name"] for artist in release["artist-credit"]]
            if set(artists_from_release) == set(artists):
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

        data = {
            "artists": [credited["artist"]["name"] for credited in response.json()["artist-credit"]],
            "title": response.json()["title"],
            "album": response.json()["release-group"]["title"],
            "release_date": response.json()["date"],
            "genres": response.json()["genres"]
        }

        return data

    def get_cover_art_url_by_id(self, id: str) -> str:
        response = requests.get(self.covert_art_url + "release/" + id)
        if response.status_code == 404:
            self.logger.warning(f"Cover art not found for release {id}")
            return None
        if response.status_code != 200:
            self.logger.error(f"Cover Art Archive API returned {response.status_code}. Response: {response.text}")
            return None

        return response.json()["images"][0]["image"]
