import os.path
from pathlib import Path
import time
from multiprocessing.dummy import Pool as ThreadPool
from spotify import Spotify
from metadata.musicbrainz import MusicBrainz
from song import Song
from logger import Logger
from lyrics.musixmatch import MusixmatchApi, MusixmatchScrapper
from download.youtube import YoutubeWeb

DOWNLOAD_PATH = "./Downloads/"
POOL_SIZE = 5

logger = Logger("Main")

musicbrainz = MusicBrainz()

musixmatch_api = MusixmatchApi()
musixmatch_api.authenticate()

musixmatch_web = MusixmatchScrapper()


def process_song(song: Song, index: int) -> bool:
    download_file_path = f"{DOWNLOAD_PATH}{index}. {str(song)}"
    file_path = f"{index}. {str(song)}"

    if os.path.isfile(f"{download_file_path}.mp4"):
        logger.info(f"{str(song)} already exists. Skipping.")
        return True

    # 3 - Get additional metadata + cover
    song_id = musicbrainz.find_song_id(title=song.title, artists=song.artists, album=song.album)
    if song_id:
        song_metadata = musicbrainz.get_metadata_by_song_id(song_id)
        logger.info(f"Metadata found: {song_metadata}")
        song.cover_url = musicbrainz.get_cover_art_url_by_id(song_id)
    else:
        logger.warning(f"No metadata found for {song.title} - {song.artists}")

    # 3.b - Alternative to MusicBrainz in case the song was not found?

    # 4 - Get the lyrics
    song_url = musixmatch_api.get_song_url(song)
    if song_url:
        song.lyrics = musixmatch_web.get_lyrics_by_song_url(song_url)
        lyrics_preview = song.lyrics.split("\n")[0]
        logger.info(f"Lyrics found, first sentence is: {lyrics_preview}")
        with open(f"{download_file_path}.txt", "w+") as f:
            f.write(song.lyrics)
    else:
        logger.warning(f"No lyrics found for {song.title} - {song.artists}")

    # 5 - Find the best match for each track (youtube, vk, zippyshare, torrent...) and download it
    youtube = YoutubeWeb()
    video_url = youtube.get_video_url(song)
    if video_url:
        logger.info(f"Video found: {video_url}")
        youtube.download_video_by_url(video_url, file_path, DOWNLOAD_PATH)


def main():

    Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)
    # 1 - Authenticate to API services
    sp = Spotify()
    sp.authenticate_oauth()

    # 1 - Get the Spotify Playlist URI from user
    # playlist_uri = input("Enter the Spotify Playlist URI: ")
    playlist_uri = "https://open.spotify.com/playlist/6NNTBfeFTJvwxK86AtSmAk?si=86ba505492964e15"

    # 2 - Get the tracks from the playlist
    tracks = sp.get_playlist_tracks_by_uri(playlist_uri)

    # 2a - Arrange the tracks in a list of Song objects
    songs = [
        Song(
            title=track["name"],
            artists=[artist["name"] for artist in track["artists"]],
            album=track["album"]["name"],
            release_date=track["album"]["name"],
            length_ms=track["duration_ms"],
        ) for track in tracks]

    logger.info(f"Found {len(songs)} tracks in the playlist.")

    pool_songs = [(song, index) for index, song in enumerate(songs)]

    pool = ThreadPool(POOL_SIZE)
    pool.starmap(process_song, pool_songs)

    pool.close()
    pool.join()


if __name__ == '__main__':
    start_time = time.time()
    main()
    duration = round(time.time() - start_time, 2)
    logger.info(f"Execution: {duration} seconds")
