"""
Custom exceptions for this project.
I can't seem to catch these properly when using Streamlit, so they may not be used =[    
"""

class SongNotPlaying(Exception):
    """ Error to inform no song was found when polling the Spotify API """
    def __init__(self, message="No song playing on Spotify!"):
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return self.message


class LyricsNotFound(Exception):
    """ Error to inform the lyrics were not found with Genius search """
    def __init__(self, artist, song):
        self.artist = artist
        self.song = song
        self.message = f"Lyrics not found for {self.artist} - {self.song}"
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
