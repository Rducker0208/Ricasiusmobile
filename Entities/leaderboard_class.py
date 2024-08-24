import json
import requests

from user_class import user

# // Load secret admin token from file
with open('./leaderboard_id.txt', 'r') as f:
    scoreboard_id = f.read()


class LeaderBoard:
    """Class used to create and update the top10 leaderboard"""

    def __init__(self):
        self.leaderboard = json.loads(load_leaderboard())['players']
        self.top_ten = {'names': [], 'scores': []}
        self.create_top_ten()

    def find_user_id(self, username: str) -> str:
        """Find the user id from the username"""

        # // Check every account for a match and fetch the correct id
        for account in self.leaderboard:
            if account['name'] == username:
                return account['id']

    def update_leaderboard(self, username: str, new_score: int) -> None:
        """Update the leaderboard to include or set a new score"""

        # // If the user exists, find them in the top10
        if username in self.top_ten['names']:

            # // if the user id is already saved
            if user.user_id:
                user_id = user.user_id
            else:
                user_id = self.find_user_id(username)
                user.user_id = user_id

            # // json to pass to the web request
            user_data = {
                         "player_id": user_id,
                         "score": new_score,
                         "operation": "set"
                         }
            requests.post(f"https://keepthescore.com/api/{scoreboard_id}/score/", json=user_data)

        # // Otherwise create a new user
        else:
            user.user_id = create_user(username, new_score)

    def create_top_ten(self) -> None:
        """Create a top ten player list which can be displayed on the leaderboard"""

        # // Load the data fram the api response
        for index, data in enumerate(self.leaderboard[:10]):
            name, score = data['name'], data['score']
            self.top_ten['names'].append(name)
            self.top_ten['scores'].append(score)


def load_leaderboard() -> str:
    """Use the requests module to load the leaderboard from keepthescore"""

    scoreboard_request = requests.get(f"https://keepthescore.com/api/{scoreboard_id}/board/")
    return scoreboard_request.text


def create_user(username: str, new_score) -> str:
    """Create a new player on the keepscore website"""

    user_data = {
        "name": username,
        "score": new_score,
        "text_color": "#FFFFFFFF",
        "background_color": "#FFC800FF",
    }

    r = requests.post(f"https://keepthescore.com/api/{scoreboard_id}/player/", json=user_data)
    user_id = json.loads(r.text)["player"]["id"]

    return user_id
