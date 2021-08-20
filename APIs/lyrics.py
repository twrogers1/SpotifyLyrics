import re

import lyricsgenius


class GeniusLyrics(lyricsgenius.Genius):
    def __init__(self, token: str):
        super().__init__(token)
        self.base_url = "https://genius.com"
        # these will be set when fetch_lyrics() is used
        self.url = None
        self.full_title = None
        self.lyric_text = None


    def _song_search_results_filter(self, artist: str, song: str, search_result: dict) -> bool:
        """
        Private Method
        Custom filter function to ensure the `artist` and `song` we searched for are found in the `search_result` from Genius's website 
        """
        assert isinstance(search_result, dict), "`search_result` should be an entry of the Genius.search() items from the [hits] array"
        
        if search_result["type"].lower() != "song":
            return False

        song = song.split("(feat.")[0].strip()  # remove the 
        
        r_artist = search_result["result"]["primary_artist"]["name"]
        r_song = search_result["result"]["title"]
        
        # explicitly find/replace these characters to ensure we don't ignore a valid match
        # sometimes different versions of the same characters are found in both places
        # or sometimes a character is missing from one source and not the other (e.g. !)
        for f,r in [
            ("’", "'"),
            ("'", ""),
            ("–", "-"),
            ("!", ""),
            (".", "")
            ]:
                artist = artist.replace(f, r)
                song = song.replace(f, r)
                r_artist = r_artist.replace(f, r)
                r_song = r_song.replace(f, r)

        return True if artist.lower() in r_artist.lower() and song.lower() in r_song.lower() else False


    def fetch_lyrics(self, artist: str, song: str):
        """ 
        Search the Genius website for the given `artist` and `song`.
        Performs validation on the search results to ensure the correct song is fetched.
        If successful, returns True and sets these instance properties in place:
            - self.url
            - self.full_title
            - self.lyric_text
        """
        song = song.split(" - ")[0]  # keep the left side of stuff like " - Acoustic" or " - Original Mix"
        search_term = artist.lower() + " " + song.lower()
        search_results = self.search(search_term, per_page=5)["hits"]  # searches for songs

        # filter the results and keep the first song that matches the song and artist
        try:
            song_info = next(filter(lambda sr: self._song_search_results_filter(artist, song, sr), search_results))
        except StopIteration:
            # since these weren't found, set them to None so we aren't using the previous values
            self.url = None
            self.full_title = None
            self.lyric_text = None
            # raise LyricsNotFound(artist, song)  # can't be caught with streamlit?
            raise KeyError(f"Lyrics not found for {artist} - {song}")
        
        song_url = self.base_url + song_info["result"]["path"]
        full_title = song_info["result"]["full_title"]
        
        # fetch lyrics with the lyircs() method and perform some cleanup:
        # line breaks are sometimes inconsistent, so we'll try to pretty it up a bit
        # add an extra line break before any section (e.g. [Chorus])
        # then convert any string of 3+ consecutive \n to only 2
        # also clean out a non-lyric phrase often presented in the data
        lyrics = self.lyrics(song_url=song_url)
        if lyrics is None:
            # no lyrics content, so we'll treat it as lyrics not found
            raise KeyError(f"Lyrics not found for {artist} - {song}")
        lyrics = re.sub(r"(\[[\w\s\d]*\]\n)", "\n\\1", lyrics, re.MULTILINE)
        lyrics = re.sub("\n{3,}", "\n\n", lyrics)
        lyrics = re.sub(r"\d*EmbedShare URLCopyEmbedCopy$", "", lyrics)
        
        self.url = song_url
        self.full_title = full_title
        self.lyric_text = lyrics
        return True


def main():
    # dev/testing
    from creds import UserCreds

    # debugging
    # import os
    # from pathlib import Path
    # os.chdir(Path().home() / "desktop" / "Github" / "SpotifyLyrics")

    user_creds = UserCreds()
    genius = GeniusLyrics(user_creds.GENIUS_TOKEN)
    
    artist = "delta sleep"
    song = "ghost"
    try:
        genius.fetch_lyrics(artist, song)
        print(genius.full_title)
        print(genius.url)
        print(genius.lyric_text)
    except KeyError as err:
        print(err)


if __name__ == "__main__":
    main()
