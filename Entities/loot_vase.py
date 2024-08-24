import random

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from music_client import music_client
from .player_class import player

# // images used
vase_image = './Resources/game_screen/loot_vase/loot_vase.png'
speed_boots_image = './Resources/game_screen/loot_vase/speed_boots.png'
shield_image = './Resources/game_screen/loot_vase/shield.png'


class LootVase:
    """Spawn a vase on screen that gives the player a power up on contact"""

    def __init__(self, root_widget: FloatLayout):
        self.root_widget = root_widget
        self.vase = Image(source=vase_image, allow_stretch=True, size_hint=(.14, .25))
        self.draw_vase()

    def draw_vase(self) -> None:
        """Draw the vase on the screen"""

        # // While loop to avoid vase spawning inside the joystick
        while True:
            x_spawnpoint = random.uniform(0, .9)
            y_spawnpoint = random.uniform(0, .63)

            if 0 <= x_spawnpoint <= .22 and 0 <= y_spawnpoint <= .4:
                pass
            else:
                break

        # // Set vase x and y position and draw it on screen
        self.vase.pos_hint = {'x': x_spawnpoint, 'y': y_spawnpoint}
        self.root_widget.add_widget(self.vase)

    def check_colision(self) -> bool:
        """Check if the player is coliding with the vase so a powerup can be spawned"""

        if abs(player.player.x - self.vase.x) < 50 and abs(player.player.y - self.vase.y) < 50:
            music_client.play_vase_breaking_sfx()
            self.root_widget.remove_widget(self.vase)
            return True
        else:
            return False
