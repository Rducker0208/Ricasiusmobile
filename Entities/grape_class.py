import random

from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from user_class import user
from .player_class import player

# // Images used
grape_image = './Resources/game_screen/grapes/grape_middle.png'


class Grapes:
    """Class that creates an image portraying a grape, this class controls the spawning off the grape
     and the deletion of it. Upon collision with the player, grant them 1 point and delete the touched grape."""

    def __init__(self):
        self.grapes_on_screen: int = 0
        self.grape_id: int = 0
        self.grapes: dict[int, Image] = {}

        # // variables for graphical purposes
        self.rotation_direction = 'right'
        self.rotation_status = 'up'
        self.rotation_angle = 0

    def create_new_grape(self, screen: Screen) -> None:
        """Create a new grape using Kivy's image class"""

        self.grape_id += 1
        self.grapes_on_screen += 1

        # // while loop to avoid grapes spawning inside the joystick
        while True:
            x_spawnpoint = random.uniform(0, .9)
            y_spawnpoint = random.uniform(0, .63)

            if 0 <= x_spawnpoint <= .22 and 0 <= y_spawnpoint <= .4:
                pass
            else:
                break

        # // Set the correct image to allign with the rest of the grapes
        if self.rotation_angle != 0:
            grape = Image(source=f'./Resources/game_screen/grapes/grape_{self.rotation_direction}'
                                 f'_{self.rotation_angle}_degrees.png', allow_stretch=True,
                          size_hint=(.15, .15), pos_hint={'x': x_spawnpoint, 'y': y_spawnpoint})
        else:
            grape = Image(source=f'./Resources/game_screen/grapes/grape_middle.png', allow_stretch=True,
                          size_hint=(.15, .15), pos_hint={'x': x_spawnpoint, 'y': y_spawnpoint})

        self.grapes[self.grape_id] = grape
        screen.add_widget(grape)

    def update_grape_rotations(self) -> None:
        """Update source image of all grapes to update animations"""

        # // check if grape is tilting more or less
        if self.rotation_status == 'up':

            # // if max rotation is reached start returning to middle point
            if self.rotation_angle == 30:
                self.rotation_status = 'down'
                self.rotation_angle -= 2
            else:
                self.rotation_angle += 2

        else:

            # // if rotation is at middle point
            if self.rotation_angle == 0:
                self.rotation_status = 'up'
                self.rotation_angle += 2

                # // change direction
                if self.rotation_direction == 'right':
                    self.rotation_direction = 'left'
                else:
                    self.rotation_direction = 'right'
            else:
                self.rotation_angle -= 2

        if self.rotation_angle == 0:
            for grape in self.grapes.values():
                grape.source = './Resources/game_screen/grapes/grape_middle.png'

        else:

            # // find grape image according to rotation and direction
            for grape in self.grapes.values():
                grape.source = (f'./Resources/game_screen/grapes/grape_{self.rotation_direction}'
                                f'_{abs(self.rotation_angle)}_degrees.png')

    def update_grapes(self, screen: Screen) -> None:
        """Update all grapes on screen and check if actions should be performed on them"""

        # // Check if player is coliding with a grape
        grapes_to_delete = []
        for grape_id, grape in self.grapes.items():
            if check_colision(grape):
                grapes_to_delete.append(grape_id)
                user.current_score += 1

        # // Delete all grapes the player is touching
        for grape_id in grapes_to_delete:
            screen.remove_widget(self.grapes[grape_id])
            self.grapes_on_screen -= 1
            del self.grapes[grape_id]

        # // Create new grape if needed
        if self.grapes_on_screen < 3:
            self.create_new_grape(screen)

        self.update_grape_rotations()


def check_colision(grape: Image) -> bool:
    """Function that checks if the player is coliding with a grape"""

    if abs(player.player.x - grape.x) < 100 and abs(player.player.y - grape.y) < 100:
        return True
    else:
        return False


grapes = Grapes()
