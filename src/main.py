from spotify import Spotify
from musicbrainz import MusicBrainz
from song import Song
from logger import Logger


def main():
    logger = Logger("Main")
    # 1 - Authenticate to Spotify
    sp = Spotify()
    sp.authenticate_oauth()

    # 1 - Get the Spotify Playlist URI from user
    # playlist_uri = input("Enter the Spotify Playlist URI: ")
    playlist_uri = "https://open.spotify.com/playlist/6NNTBfeFTJvwxK86AtSmAk?si=86ba505492964e15"

    # 2 - Get the tracks from the playlist
    tracks = sp.get_playlist_tracks_by_uri(playlist_uri)

    # 2a - Arrange the tracks in a list of Song objects
    songs = []
    for track in tracks:
        song = Song(
            title=track["name"],
            artists=[artist["name"] for artist in track["artists"]],
            album=track["album"]["name"],
            release_date=track["album"]["name"],
            length_ms=track["duration_ms"],
        )
        songs.append(song)

    # 3 - Get additional metadata + cover (musicbrainz.org) for each track
    mb = MusicBrainz()
    for song in songs:
        song_id = mb.find_song_id(title=song.title, artists=song.artists, album=song.album)
        logger.info(f"Song id is:{song_id}")
        if song_id:
            response = mb.get_metadata_by_song_id(song_id)
            logger.info(f"Metadata: {response}")
            cover = mb.get_cover_art_url_by_id(song_id)
            logger.info(f"Cover: {cover}")
    # 4 - Get the lyrics (genius.com / musixmatch.com) for each track

    # 4 - Find the best match for each track (youtube, vk, zippyshare, torrent...)

    # 5 - Download the best match


if __name__ == '__main__':
    main()
