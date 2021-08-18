@echo off

cd  %~dp0

title Spotify Lyrics
color 0A

echo Starting SpotifyLyrics...
call venv\Scripts\activate.bat
call streamlit run main.py