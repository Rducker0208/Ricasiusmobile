import sqlite3


class database:
    """sqlite3 database that is used to check a user's highscore"""

    def __init__(self, user: str):
        self.user = user

        # // creates a connection to the database
        self.connection = sqlite3.connect('highscores.db')

    def load_user(self) -> str:
        """function that loads a user's highscore from the database"""

        # // cursor is used to make requests to database
        cursor = self.connection.cursor()

        # // try to find user in database and get their highscore
        cursor.execute("SELECT * FROM highscores WHERE username=:username", {'username': self.user})
        result = cursor.fetchone()

        # // if user doesn't exist in database add them and otherwise return their highscore
        if not result:
            cursor.execute("INSERT INTO highscores VALUES(:username, :score)",
                           {'username': self.user, 'score': 0})
            self.connection.commit()
            return '0'
        else:
            return result[1]

    def update_user(self, score: int) -> None:
        """Function to update a user's highscore in the database if they surpass it"""

        # // cursor is used to make requests to database
        cursor = self.connection.cursor()

        cursor.execute("UPDATE highscores SET username=:username, score=:score WHERE username=:username",
                       {'username': self.user, 'score': score})
        self.connection.commit()
