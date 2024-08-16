import sqlite3


class database:
    """sqlite3 database that is used to check a user's highscore"""

    def __init__(self):

        # // creates a connection to the database
        self.connection = sqlite3.connect('./user_data.db')

    def load_user_info(self, username: str) -> tuple[str, str]:
        """Load user settings from the databse"""

        # // cursor is used to make requests to database
        cursor = self.connection.cursor()

        # // get user info from the database
        request = cursor.execute(f"SELECT * FROM user_data WHERE name='{username}'")
        user_info = request.fetchone()

        # // if the user exists return their info, else create a user
        if user_info:
            return user_info[1:]
        else:
            cursor.execute("INSERT INTO user_data VALUES(?, ?, ?)", (username, '0', '{}'))
            self.connection.commit()

            return '0', '{}'

    def update_user_settings(self):
        ...

    def update_user_score(self, username: str, new_score: int):
        """Function to update a user's highscore in the database if they surpass it"""

        if username == 'None' or not username:
            return
        else:
            # // cursor is used to make requests to database
            cursor = self.connection.cursor()

            # // update the user score in the database
            cursor.execute(f"""UPDATE user_data SET highscore='{new_score}' WHERE name='{username}'""")
            self.connection.commit()

            cursor.execute("SELECT * FROM user_data")


db = database()