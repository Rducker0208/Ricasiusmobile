from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from .player_class import player

# // images used
# // Images created on: https://pinetools.com/merge-images
heart_dir = './Resources/game_screen/hearts'


class Hp:
    """Class used to keep track of the player's hp and display the according sprite on screen"""

    def __init__(self):
        self.hearts = Image(source=f'{heart_dir}/5_hp.png', allow_stretch=True,
                            size_hint=(.2, .1), pos_hint={'x': .01, 'y': .9})

    def update_hp(self, screen: Screen) -> None:
        """Function that updates the hp sprite"""

        screen.remove_widget(self.hearts)
        self.hearts.source = f'{heart_dir}/{player.hp}_hp.png'
        screen.add_widget(self.hearts)


hp = Hp()
