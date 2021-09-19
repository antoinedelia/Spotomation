from pytube import YouTube
from youtube_search import YoutubeSearch
from models.song import Song
from logger import Logger
from datetime import timedelta


class YoutubeWeb:
    def __init__(self) -> None:
        self.logger = Logger("Youtube")

    def get_video_url(self, song: Song) -> str:
        artists_as_string = ' '.join(song.artists)
        song_query = f"{song.title} {artists_as_string} audio"

        self.logger.info(f"Searching for song: {song_query}")

        try:
            results = YoutubeSearch(song_query, max_results=5).to_dict()
        except Exception as e:
            self.logger.error(f"Exception while searching song: {song_query}. Exception was: {e}")
            return None

        if len(results) == 0:
            self.logger.warning(f"No results for query: {song_query}")
            return None

        # Try to find the most exact match based on duration
        possible_matches = []
        for result in results:
            video_duration = result['duration']

            hours, minutes, seconds = 0, 0, 0
            if video_duration.count(':') == 1:
                minutes, seconds = map(float, video_duration.split(':'))
            else:
                hours, minutes, seconds = map(float, video_duration.split(':'))

            video_duration_ms = int(timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds() * 1000)

            # We consider 5 seconds to be a good match
            if abs(video_duration_ms - song.length_ms) < 5000:
                possible_matches.append(result)

        if len(possible_matches) == 0:
            self.logger.info(f"No exact match found for song: {song_query}")
            video_url = 'http://youtu.be' + results[0]['url_suffix'].replace('watch?v=', '')
            return video_url

        video_url = 'http://youtu.be' + possible_matches[0]['url_suffix'].replace('watch?v=', '')
        return video_url

    def download_video_by_url(self, url: str, mp4_path: str) -> None:
        youtube = YouTube(url).streams.get_audio_only()
        directory, filename = mp4_path.rsplit('/', 1)
        youtube.download(directory, filename=filename)
