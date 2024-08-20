from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from .player_class import player

# // images used
speed_boots_image = './Resources/game_screen/loot_vase/speed_boots.png'


class SpeedBoots:
    """Class containing speed boots, a powerup that grants the player 1.5 times their speed for 15 seconds"""

    def __init__(self):

        # // Image and label used to graphically display this powerup
        self.speed_shoes = Image(source=speed_boots_image, allow_stretch=True,
                                 size_hint=(.1, .1), pos_hint={'x': .92, 'y': .9})
        self.time_left_lable = Label(text='0', font_size=64, color='black',
                                     size_hint=(.1, .1), pos_hint={'x': .86, 'y': .9})
        self.root_widget: FloatLayout | None = None

        self.active = False
        self.time_left = 0
        self.update_loop = None

    def draw_boots(self, root_widget: FloatLayout) -> None:
        """Draw speed boots on screen"""

        self.root_widget = root_widget

        self.time_left = 15
        self.time_left_lable.text = str(self.time_left)
        self.root_widget.add_widget(self.speed_shoes)
        self.root_widget.add_widget(self.time_left_lable)

        self.update_loop = Clock.schedule_interval(self.update_time_left, 1)
        Clock.schedule_once(self.remove_boots, 15)

        player.base_speed *= 1.5
        self.active = True

    def remove_boots(self, dt) -> None: # noqa
        """Remove speed boots from screen"""

        self.root_widget.remove_widget(self.time_left_lable)
        self.root_widget.remove_widget(self.speed_shoes)
        self.update_loop.cancel()
        self.active = False
        player.base_speed /= 1.5

    def update_time_left(self, dt) -> None: # noqa
        """Update the time left lable"""

        self.time_left -= 1
        self.time_left_lable.text = str(self.time_left)


speed_boots = SpeedBoots()
