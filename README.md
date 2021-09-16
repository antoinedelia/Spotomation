# Spotify 2 Mp3

## Getting Started

Create a new application in the [Spotify Dashboard](https://developer.spotify.com/dashboard/applications).

```shell
$ pip install -r requirements.txt

# Spotify Credentials
$ export SPOTIPY_CLIENT_ID='your-client-id'
$ export SPOTIPY_CLIENT_SECRET='your-client-secret' 

# Genius Credentials
$ export GENIUS_CLIENT_ID='your-client-id'
$ export GENIUS_CLIENT_SECRET='your-client-secret' 

# Musixmatch Credentials
$ export MUSIXMATCH_API_KEY='your-api-key' 

$ python src/main.py
```

## Known Issues

We can't really get the lyrics, as both the Genius and MusixMatch APIs are limited. [Genius simply doesn't allow to return the lyrics for a song](https://genius.com/discussions/277279-Get-the-lyrics-of-a-song), while [Musixmatch only return 30% of the lyrics for a song](https://developer.musixmatch.com/faq).

## Built with

- Requests (http api calls)
- Spotipy (Spotify Python client)
- MusicBrainz (metadata)
- Cover Art Archive (cover art)
- Genius/Musixmatch (lyrics)
