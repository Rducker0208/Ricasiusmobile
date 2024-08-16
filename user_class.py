from database_class import db


class User:
    """Class containing all needed user data"""

    def __init__(self):
        self.username = get_username()
        self.highscore = None
        self.user_settings = None

        if self.username:
            user_info = db.load_user_info(self.username)
            self.highscore = int(user_info[0])
            self.user_settings = eval(user_info[1])

            print(self.highscore)

        self.current_score = 0


def get_username() -> str | None:
    """Use os module to see if user is on windows and otherwise use plyer to get user id"""

    with open('username.txt') as f:
        file_content = f.read()
        if file_content:
            return file_content
        else:
            return None


user = User()
