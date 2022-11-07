***Note: this project is now obsolete as Spotify has first party support for lyrics in their desktop and mobile apps.***

# SpotifyLyrics

Display lyrics for your currently playing Spotify track within a Streamlit webapp.

![Preview](/img/preview.png)

# Setup and Requirements

This project was built and tested with Python 3.9 on Windows and Mac. The primary external modules used are `streamlit`, `spotipy`, `lyricsgenius`, and `python-dotenv`. You will need your own Spotify and Genius.com app tokens.

If you're not familiar with setting up a virtual environment and pip installing packages, follow the guide below:

1. Download this project
2. Create a Python virtual environment called `\venv` within the project directory. Open terminal/cmd, `cd` into this directory, and create the virtual environment:
	- *Streamlit is recommended to run in a virtual environment and behaves strangely when the global environment is used*
	- Windows: `python -m venv venv`
	- Mac: `python3 -m venv venv`
3. Activate the new virtual environment:
	- Windows: `venv\Scripts\activate.bat`
	- Mac: `source ./bin/activate`
4. Install dependencies using pip: `pip install -r setup\requirements.txt`, and allow several seconds to complete

Next, we need to acquire our tokens and store them locally in an environment file:

1. In the project directory, rename the `.env_sample` file to `.env` and open with a text editor
2.  To set the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` values, visit https://developer.spotify.com/dashboard/applications and create a new app
	- Ensure the redirect URI matches between the app you create and the `.env` file
	- https://google.com should be fine
3. To set the `GENIUS_TOKEN` value, browse to https://genius.com/api-clients and create a new app
4. Save the file


# Launching App and First Time Use

To launch the application, Windows users can double-click the `start.bat` file in the project's root directory.

To launch manually, ensure your terminal has the virtual environment active and the current directory is the project's directory, then issue this command: `streamlit run main.py`.

On first launch, (or whenever the `.cache` file is not found), you will need to sign in to Spotify. When Streamlit is launched, your default browser will open a new Streamlit window. A secondary tab will open, prompting to sign in to Spotify. After signing in, you will be forwarded to the redirect URI with a code appended (e.g. https://www.google.com/?code=xxxxx). Copy this entire url and paste in your terminal, where you should see a prompt like the following: `Enter the URL you were redirected to: `.  After hitting enter, you should now be authenticated.
