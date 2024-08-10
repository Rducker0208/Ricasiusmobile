import os
import PIL.Image

from plyer.facades import UniqueID
from database_class import db


class User:
    """Class containing all needed user data"""

    def __init__(self):
        self.username = get_username()
        self.highscore = db.load_user(self.username)
        self.current_score = 0

    def create_score_image(self, mode: str) -> None:
        """Use pillow to create a new image portraying the users highscore in a special font"""

        # // gather all images and their total width
        if mode == 'highscore':
            images = [PIL.Image.open(rf'./Resources/numbers/{number}.png') for number in str(self.highscore)]
        else:
            images = [PIL.Image.open(rf'./Resources/numbers/{number}.png') for number in str(self.current_score)]

        total_width = sum([image.size[0] for image in images])

        # // create a new image
        new_image = PIL.Image.new('RGBA', (total_width, 63))

        # // go through all images and add them to the new image, increase offset so images don't merge together
        x_offset = 0
        for image in images:
            new_image.paste(image, (x_offset, 0))
            x_offset += image.size[0]

        if mode == 'highscore':
            new_image.save('./Resources/start_screen/highscore.png')
        else:
            new_image.save('./Resources/game_over_screen/score.png')


def get_username() -> str:
    """Use os module to see if user is on windows and otherwise use plyer to get user id"""

    if os.name == 'nt':
        user_name = os.getlogin()
    else:
        user_name = str(UniqueID.id)
        print(f'user: {user_name}')

    return user_name


user = User()
