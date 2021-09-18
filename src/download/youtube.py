from pytube import YouTube
from youtube_search import YoutubeSearch
from song import Song
from logger import Logger


class YoutubeWeb:
    def __init__(self) -> None:
        self.logger = Logger("Youtube")

    def get_video_url(self, song: Song) -> str:
        artists_as_string = ' '.join(song.artists)
        song_query = f"{song.title} {artists_as_string} audio"

        self.logger.info(f"Searching for song: {song_query}")

        results = YoutubeSearch(song_query, max_results=1).to_dict()

        if len(results) == 0:
            self.logger.warning(f"No results for query: {song_query}")
            return None

        video_url = 'http://youtu.be' + results[0]['url_suffix'].replace('watch?v=', '')
        return video_url

    def download_video_by_url(self, url: str, mp4_path: str) -> None:
        youtube = YouTube(url).streams.get_audio_only()
        directory, filename = mp4_path.rsplit('/', 1)
        youtube.download(directory, filename=filename)
