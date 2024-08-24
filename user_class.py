from database_class import db


class User:
    """Class that is used for storing all the user data that is needed to make the app function,
     like settings and username."""

    def __init__(self):
        self.username = get_username()
        self.user_id = None
        self.user_settings = None
        self.highscore = None

        # // If the user is logged in load their data
        if self.username:
            user_info = db.load_user_info(self.username)
            self.highscore = int(user_info[0])
            self.user_settings = eval(user_info[1])

        self.current_score = 0


def get_username() -> str | None:
    """Check if the user has logged in before,
    if not set the name to None so the login screen will be triggered"""

    with open('username.txt') as f:
        file_content = f.read()
        if file_content:
            return file_content
        else:
            return None


user = User()
