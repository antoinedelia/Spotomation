# Spotify 2 Mp3

## Prerequisites

Install [ffmpeg](https://www.ffmpeg.org/download.html).

Create a new application in the [Spotify Dashboard](https://developer.spotify.com/dashboard/applications) to get your client id and client secret.

Create a new application in the [Musixmatch Dashboard](https://developer.musixmatch.com/admin) to get your api key.

## Getting Started

```shell
$ pip install -r requirements.txt

# Spotify Credentials
$ export SPOTIPY_CLIENT_ID='your-client-id'
$ export SPOTIPY_CLIENT_SECRET='your-client-secret' 

# Musixmatch Credentials
$ export MUSIXMATCH_API_KEY='your-api-key' 

$ python src/main.py
```

## FAQ

### Why can't you get the lyrics directly from the API?

We can't really get the lyrics, as both the Genius and MusixMatch APIs are limited. [Genius simply doesn't allow to return the lyrics for a song](https://genius.com/discussions/277279-Get-the-lyrics-of-a-song), while [Musixmatch only return 30% of the lyrics for a song](https://developer.musixmatch.com/faq).

## Built with

- [requests](https://docs.python-requests.org/en/latest/) (http api calls)
- [spotipy](https://spotipy.readthedocs.io/en/2.19.0/) (Spotify Python client)
- [MusicBrainz](https://musicbrainz.org/doc/MusicBrainz_API) (metadata)
- [Cover Art Archive](https://musicbrainz.org/doc/Cover_Art_Archive/API) (cover art)
- [Musixmatch](https://www.musixmatch.com/) (lyrics/ cover art)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (html parsing)
- [ffmpeg](https://www.ffmpeg.org/) (conversion)
- [pytube](https://pytube.io/en/latest/) (Youtube video downloader)
- [youtube-search](https://github.com/joetats/youtube_search) (Youtube video search)
- [eyeD3](https://eyed3.readthedocs.io/en/latest/) (ID3 tags)