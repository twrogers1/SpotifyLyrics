import datetime as dt
import json
from pathlib import Path
from textwrap import dedent

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Track:
    """ A class to represent the data from the Spotify API for the current track. """ 
    def __init__(self, data: dict):
        if data is None or data["is_playing"] == False:
            # raise SongNotPlaying()  # can't be caught with streamlit?
            raise FileNotFoundError("No song playing on Spotify!")
        
        self.data = data  # the raw json object / dict from Spotify's API
        self.id = data["item"]["id"]
        self.artist = data["item"]["artists"][0]["name"]
        self.song = data["item"]["name"]
        self.album = data["item"]["album"]["name"]
        self.release_year = data["item"]["album"]["release_date"][:4]

        try:
            # try to get the album art at a certain size
            album_images = data["item"]["album"]["images"]
            # heights = 640, 300, 64
            self.art = next(filter(lambda x: x["height"] == 300, album_images))["url"]
        except StopIteration:
            # if that size wasn't found, just grab the first one
            self.art = album_images[0]["url"]
        
        self.song_data_dir = Path().parent / "SongData"
        if not self.song_data_dir.exists():
            self.song_data_dir.mkdir()
        

    def __str__(self):
        if self.song is not None:
            return dedent(f"""
            {self.artist} - {self.song}
            {self.album} ({self.release_year})
            """)
        else:
            return None


    def __eq__(self, other):
        """ When comparing two Track objects, use their `ids` """
        if other is None or self.id != other.id:
            return False
        else:
            return True


    def save(self):
        """ Write the raw track json data to file. Mostly used for debugging when running this file as __main__ """
        if self.song is None:
            return
        
        track_info_file = self.song_data_dir / "track_info.json"
        with track_info_file.open("w") as f:
            json.dump(self.data, f, indent=4)
        
        print(f"Saved [{self.artist} - {self.song}] track data to {self.song_data_dir.absolute()}.")
        return


def main():
    # dev/testing
    
    # debugging
    # import os
    # os.chdir(Path().home() / "Desktop" / "Github" / "SpotifyLyrics")

    import time

    from creds import UserCreds

    user_creds = UserCreds()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=user_creds.SPOTIPY_CLIENT_ID,
            client_secret=user_creds.SPOTIPY_CLIENT_SECRET,
            redirect_uri=user_creds.SPOTIPY_REDIRECT_URI,
            scope=user_creds.scope
        )
    )
    
    last_track = None
    while True:
        try:
            now_playing = sp.currently_playing()
            track = Track(now_playing)

            if last_track != track:
                track.save()
                print(track)
        
            last_track = track
        except FileNotFoundError as err:
            print(err)
        
        time.sleep(5)


if __name__ == "__main__":
    main()
