from dataclasses import dataclass, field


@dataclass
class Song():
    """
    Class for song objects
    """
    title: str
    artists: list
    album: str
    year: int
    length_ms: int
    genre: str = None
    lyrics: str = None
    cover_url: str = None
    possible_download_urls: list = field(default_factory=list)

    def __str__(self):
        """
        String representation of song object
        """
        return f"{self.title} - {self.artists} - {self.album}"

    def __repr__(self):
        """
        String representation of song object
        """
        return f"{self.title} - {self.artists} - {self.album}"
