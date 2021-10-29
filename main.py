import time
import datetime as dt

import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth

from APIs.creds import UserCreds
from APIs.lyrics import GeniusLyrics
from APIs.spotify import Track


def getdate():
    """ Return the current timestamp """
    return str(dt.datetime.now())


def main():
    st.set_page_config(
        page_title="Spotify Lyrics",
        layout="centered",  # centered, wide
        initial_sidebar_state="collapsed",
        page_icon="🎵"
    )

    print("\n" + f"{getdate()} Running script.")

    with st.sidebar:
        st.markdown("""
        ## API Token Quick Links
        - **Spotify**: https://developer.spotify.com/dashboard/applications
        - **Genius**: https://genius.com/api-clients
        """)

    user_creds = UserCreds()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=user_creds.SPOTIPY_CLIENT_ID,
        client_secret=user_creds.SPOTIPY_CLIENT_SECRET,
        redirect_uri=user_creds.SPOTIPY_REDIRECT_URI,
        scope=user_creds.scope
    )
    )
    genius = GeniusLyrics(user_creds.GENIUS_TOKEN)

    # the st.empty() container-like object stores the page's contents
    # when a new song is detected, we'll flush this object and display the new stuff
    # we're effectively refreshing the screen for the user so they don't have to
    page = st.empty()

    # routinely scan for new tracks and fetch lyrics when the track changes
    # the try/except nesting here is a bit gross,
    # but it's done this way to try to keep the screen pretty to the user when errors occur
    # and try to prevent them from having to refresh manually
    last_track = None
    while True:
        try:
            now_playing = sp.currently_playing()
            track = Track(now_playing)

            if last_track != track:
                print(f"{getdate()}: Current Track: " + "\n" + str(track))
                page.empty()
                with page.container():
                    img, title = st.columns([2, 4])
                    with img:
                        st.image(track.art)

                    with title:
                        st.markdown(f"""
                        ### {track.song}
                        #### 🎤 {track.artist}
                        💿 {track.album} ({track.release_year})
                        """)

                    try:
                        with st.spinner(text="Fetching lyrics..."):
                            print(f"{getdate()}: Fetching lyrics for {track.artist} - {track.song}...")
                            genius.fetch_lyrics(track.artist, track.song)
                            print(f"{getdate()}: Done.")
                            # finish formatting lyric text
                            lyrics = genius.full_title + "\n\n" + genius.lyric_text
                            lyrics = lyrics.replace("\n\n\n",
                                                    "\n\n")  # sometimes we get too many line breaks introduced

                        st.subheader("Lyrics")
                        st.code(lyrics, language=None)
                        st.caption(genius.url)
                    except KeyError as e:  # LyricsNotFound
                        st.warning(e)

            last_track = track
        except FileNotFoundError as e:  # SongNotPlaying
            page.empty()
            with page.container():
                st.warning(e)
        finally:
            time.sleep(1)


if __name__ == "__main__":
    main()
