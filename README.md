# Spotify 2 Mp3

## Getting Started

Create a new application in the [Spotify Dashboard](https://developer.spotify.com/dashboard/applications).

Make sure to set the `Redirect URIs` to `http://localhost:8080` in the settings.

```shell
$ pip install -r requirements.txt

$ export SPOTIPY_CLIENT_ID='your-client-id'
$ export SPOTIPY_CLIENT_SECRET='your-client-secret' 
$ export SPOTIPY_REDIRECT_URI='http://localhost:8080'

$ python src/main.py
```

## Built with

- Requests (http api calls)
- Spotipy (Spotify Python client)
- MusicBrainz (metadata)
- Cover Art Archive (cover art)
- Genius/Musixmatch (lyrics)
