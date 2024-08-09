import random

from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import Screen

from player_class import Player
from user_class import User

# // Images used
grape_image = './Resources/game_screen/grape.png'


class Grapes:
    """class that handles the grapes that give points"""

    def __init__(self):
        self.grapes_on_screen: int = 0
        self.grape_id: int = 0
        self.grapes: dict[int, Image] = {}

        # // variables for graphical purposes
        self.angle = 24
        self.rotation_direction = 'right'

    def create_grape(self, screen: Screen) -> None:
        """Create a new grape using Kivy's scatter widget, the Scatter widget provides
        rotation support for the animation of the grapes"""

        self.grape_id += 1
        self.grapes_on_screen += 1

        grape = Scatter(do_scale=False, do_rotation=False, do_translation=False, rotation=0,
                        scale=1.2, pos_hint={'x': random.uniform(0, .9),
                                             'y': random.uniform(0, .63)})

        # // add the grape image to the Scatter widget and add the Scatter widget to the screen
        grape.add_widget(Image(source=grape_image))
        self.grapes[self.grape_id] = grape
        screen.add_widget(grape)

    def animate_grape(self, grape: Scatter) -> None:
        """Animate the grape using Kivy's Scatter widget's rotation variable"""

        if self.rotation_direction == 'right':
            grape.rotation += 2
        else:
            grape.rotation -= 2

            # self.angle += 2
            #
            # if self.angle == 24:
            #     self.rotation_direction = 'left'

    def update_grapes(self, screen: Screen, player: Player, user: User):
        grapes_to_delete = []

        for grape_id, grape in self.grapes.items():
            if check_colision(grape, player):
                grapes_to_delete.append(grape_id)
                user.current_score += 1

        for grape_id in grapes_to_delete:
            screen.remove_widget(self.grapes[grape_id])
            self.grapes_on_screen -= 1
            del self.grapes[grape_id]

        if self.grapes_on_screen < 3:
            self.create_grape(screen)
        #
        # for grape in self.grapes.values():
        #     self.animate_grape(grape)

        if self.rotation_direction == 'right':
            if self.angle == 24:
                self.rotation_direction = 'left'
            else:
                self.angle += 2

        else:
            pass


def check_colision(grape: Image, player: Player) -> bool:
    """Function that checks if the player is coliding with a grape"""

    if abs(player.player.x - grape.x) < 100 and abs(player.player.y - grape.y) < 100:
        return True
    else:
        return False
