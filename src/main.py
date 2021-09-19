import argparse
import os
import subprocess
from pathlib import Path
import time
from multiprocessing.dummy import Pool as ThreadPool
import eyed3
from eyed3.id3.frames import ImageFrame
from eyed3.id3 import ID3_V2_3
from tqdm import tqdm
import istarmap  # noqa F401
from spotify import Spotify
from metadata.musicbrainz import MusicBrainz
from song import Song
from logger import Logger
from lyrics.musixmatch import MusixmatchApi, MusixmatchScrapper
from download.youtube import YoutubeWeb

parser = argparse.ArgumentParser()

parser.add_argument('--delete', '-d', required=False, action='store_true',
                    help='Delete the destination folder before starting',
                    dest='should_delete')

args = parser.parse_args()

SHOULD_DELETE = args.should_delete

DOWNLOAD_PATH = "./Downloads/"
POOL_SIZE = 5

logger = Logger("Main")

musicbrainz = MusicBrainz()

musixmatch_api = MusixmatchApi()
musixmatch_api.authenticate()

musixmatch_web = MusixmatchScrapper()


def get_lyrics(song: Song) -> str:
    song_url = musixmatch_api.get_song_url(song)
    if song_url:
        return musixmatch_web.get_lyrics_by_song_url(song_url)
    else:
        logger.warning(f"No lyrics found for {song.title} - {song.artists}")
        return None


def get_cover_art_url(song: Song) -> str:
    song_url = musixmatch_api.get_song_url(song)
    if song_url:
        cover_url = musixmatch_web.get_cover_url_by_song_url(song_url)
        if cover_url:
            return cover_url
    song_id = musicbrainz.find_song_id(title=song.title, artists=song.artists, album=song.album)
    if song_id:
        return musicbrainz.get_cover_art_url_by_id(song_id)
    return None


def get_metadata(song: Song) -> dict:
    song_id = musicbrainz.find_song_id(title=song.title, artists=song.artists, album=song.album)
    if song_id:
        return musicbrainz.get_metadata_by_song_id(song_id)
    return None


def download_song(song: Song, mp4_path: str):
    youtube = YoutubeWeb()
    video_url = youtube.get_video_url(song)
    if video_url:
        logger.info(f"Video found: {video_url}")
        youtube.download_video_by_url(video_url, mp4_path)


def process_song(song: Song, index: int) -> bool:
    LYRICS_PATH = f"{DOWNLOAD_PATH}{index}. {str(song)}.txt"
    MP4_PATH = f"{DOWNLOAD_PATH}{index}. {str(song)}.mp4"
    MP3_PATH = f"{DOWNLOAD_PATH}{index}. {str(song)}.mp3"

    if os.path.isfile(MP3_PATH):
        logger.info(f"{str(song)} already exists. Skipping.")
        return True

    # Trying to get cover url
    song.cover_url = get_cover_art_url(song)

    # Get the lyrics
    if os.path.isfile(LYRICS_PATH):
        logger.info(f"Lyrics for {str(song)} already exist.")
    else:
        song.lyrics = get_lyrics(song)
        with open(LYRICS_PATH, "w+") as f:
            f.write(song.lyrics)

    # Find the best match for each track (youtube, vk, zippyshare, torrent...) and download it
    if os.path.isfile(MP4_PATH):
        logger.info(f"MP4 file for {str(song)} already exist.")
    else:
        download_song(song, MP4_PATH)

    # Convert from mp4 to mp3
    subprocess.run(['ffmpeg', '-i', MP4_PATH, MP3_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Add the cover art to the mp3 file
    if song.cover_url:
        audiofile = eyed3.load(MP3_PATH)
        if (audiofile.tag is None):
            audiofile.initTag()

        import requests
        image = requests.get(song.cover_url, stream=True)
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, image.content, 'image/jpeg')

        audiofile.tag.save(version=ID3_V2_3)
        logger.info(f"Cover art {song.cover_url} added to {str(song)}")


def main():
    if SHOULD_DELETE:
        logger.info("Deleting destination folder...")
        import shutil
        shutil.rmtree(DOWNLOAD_PATH, ignore_errors=True)
    Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)

    # Get the Spotify Playlist URI from user
    # playlist_uri = input("Enter the Spotify Playlist URI: ")
    playlist_uri = "https://open.spotify.com/playlist/0JP3smzah2mTnxIZIVjVX0?si=28b345b00c9941be"

    # Get the tracks from the playlist
    sp = Spotify()
    sp.authenticate_oauth()
    tracks = sp.get_playlist_tracks_by_uri(playlist_uri)

    # Arrange the tracks in a list of Song objects
    songs = [
        Song(
            title=track["name"],
            artists=[artist["name"] for artist in track["artists"]],
            album=track["album"]["name"],
            release_date=track["album"]["name"],
            length_ms=track["duration_ms"],
        ) for track in tracks]

    logger.info(f"Found {len(songs)} tracks in the playlist.")

    pool_songs = [(song, index+1) for index, song in enumerate(songs)]

    pool = ThreadPool(POOL_SIZE)

    for _ in tqdm(pool.istarmap(process_song, pool_songs), total=len(pool_songs)):
        pass

    pool.close()
    pool.join()


if __name__ == '__main__':
    start_time = time.time()
    main()
    duration = round(time.time() - start_time, 2)
    logger.info(f"Execution: {duration} seconds")
