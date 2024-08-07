from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

# // images used
heart_dir = './Resources/game_screen/hearts'


class hp:
    """Class used to keep track of player hp and draw hearts on screen to indicate this"""

    def __init__(self):
        self.hearts = Image(source=f'{heart_dir}/5_hp.png', allow_stretch=True,
                            size_hint=(.3, .15), pos_hint={'x': .01, 'y': .85})

    def update_hp(self, screen: Screen, player) -> None:
        """Function that updates healthbar"""

        screen.remove_widget(self.hearts)
        self.hearts.source = f'{heart_dir}/{player.hp}_hp.png'
        screen.add_widget(self.hearts)
