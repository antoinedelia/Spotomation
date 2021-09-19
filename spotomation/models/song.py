from dataclasses import dataclass, field


@dataclass
class Song():
    """
    Class for song objects
    """
    title: str
    artists: list
    album: str
    release_date: str
    length_ms: int
    genres: list = field(default_factory=list)
    lyrics: str = None
    cover_url: str = None
    possible_download_urls: list = field(default_factory=list)

    def __str__(self):
        """
        String representation of song object
        """
        artists = " & ".join(self.artists)
        return f"{artists} - {self.title}"

    def __repr__(self):
        """
        String representation of song object
        """
        artists = " & ".join(self.artists)
        return f"{artists} - {self.title}"
