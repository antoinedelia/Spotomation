from spotify import Spotify
from song import Song


def main():
    # 1 - Authenticate to Spotify
    sp = Spotify()
    sp.authenticate_oauth()

    # 1 - Get the Spotify Playlist URI from user
    # playlist_uri = input("Enter the Spotify Playlist URI: ")
    playlist_uri = "https://open.spotify.com/playlist/0JP3smzah2mTnxIZIVjVX0?si=4e733139dce8416a"

    # 2 - Get the tracks from the playlist
    tracks = sp.get_playlist_tracks_by_uri(playlist_uri)

    # 2a - Arrange the tracks in a list of Song objects
    songs = []
    for track in tracks:
        song = Song(
            title=track["name"],
            artists=[artist["name"] for artist in track["artists"]],
            album=track["album"]["name"],
            year=track["album"]["name"],
            length_ms=track["duration_ms"],
        )
        songs.append(song)

    for song in songs:
        print(song)
    # 3 - Get additional metadata + cover + lyrics for each track

    # 4 - Find the best match for each track (youtube, vk, zippyshare, torrent...)

    # 5 - Download the best match


if __name__ == '__main__':
    main()
