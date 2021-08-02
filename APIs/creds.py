from pathlib import Path

from dotenv import dotenv_values


class UserCreds():
    """
    A simple class to store user credentials to be passed to the spotipy client.
    No other funtionality supported at this time.
    """
    def __init__(self):
        env_path = Path().parent / ".env"
        env = dotenv_values(env_path)
        self.SPOTIPY_CLIENT_ID = env["SPOTIPY_CLIENT_ID"]
        self.SPOTIPY_CLIENT_SECRET= env["SPOTIPY_CLIENT_SECRET"]
        self.SPOTIPY_REDIRECT_URI = env["SPOTIPY_REDIRECT_URI"]
        self.GENIUS_TOKEN = env["GENIUS_TOKEN"]
        self.scope = "user-read-currently-playing"


    def __str__(self):
        banner_len = 55
        string = "**** Secrets ".ljust(banner_len, "*") + "\n"
        for k, v in self.__dict__.items():
            string += f"{k} : {v}" + "\n"
        string += "*" * banner_len
        return string


def main():
    user_creds = UserCreds()
    print(user_creds)
    

if __name__ == "__main__":
    main()
