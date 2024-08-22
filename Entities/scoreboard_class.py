import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()
scoreboard_id = os.getenv("SCOREBOARD_ID")


class ScoreBoard:

    def __init__(self):
        self.scoreboard = json.loads(load_scoreboard())
        self.top_ten = {'names': [], 'scores': []}
        self.create_top_ten()

    def update_scoreboard(self):
        ...

    def create_top_ten(self) -> None:
        """Create a top ten player list which can be displayed on the leaderboard"""

        raw_top_ten = self.scoreboard['players'][:10]

        # // Load the data fram the api response
        for index, data in enumerate(raw_top_ten):
            name, score = data['name'], data['score']
            self.top_ten['names'].append(name)
            self.top_ten['scores'].append(score)


def load_scoreboard() -> str:
    """Use the requests module to load the scoreboard from keepthescore"""

    scoreboard_request = requests.get(f"https://keepthescore.com/api/{scoreboard_id}/board/")
    return scoreboard_request.text


scoreboard = ScoreBoard()