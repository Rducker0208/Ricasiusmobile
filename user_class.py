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

    def create_score_image(self, mode: str) -> None:
        """Use pillow to create a new image portraying the users (high)score in a special font"""

        # print(f'creating image for {self.username}, score: {self.highscore}')
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
            # // remove old file
            p = pathlib.Path('./Resources/start_screen/highscore.png')
            pathlib.Path.unlink(p, missing_ok=True)

            # // save new file
            new_image.save('./Resources/start_screen/highscore.png')
        else:
            # // remove old file
            p = pathlib.Path('./Resources/game_over_screen/score.png')
            pathlib.Path.unlink(p, missing_ok=True)

            new_image.save('./Resources/game_over_screen/score.png')


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
