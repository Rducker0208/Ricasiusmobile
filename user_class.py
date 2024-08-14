import os
import pathlib
import PIL.Image

from database_class import db


class User:
    """Class containing all needed user data"""

    def __init__(self):
        self.username = get_username()

        if self.username:
            self.highscore = db.load_user(self.username)
        else:
            self.highscore = 0

        self.current_score = 0


def get_username() -> str | None:
    """Use os module to see if user is on windows and otherwise use plyer to get user id"""

    if os.name == 'ntpy':
        user_name = os.getlogin()
        return user_name

    else:
        with open('username.txt') as f:
            file_content = f.read()
            if file_content:
                return file_content
            else:
                return None


user = User()
