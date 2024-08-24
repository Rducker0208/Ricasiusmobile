from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from music_client import music_client

# // images used
shield_image = './Resources/game_screen/loot_vase/shield.png'


class Shield:
    """A powerup obtained via a lootvase, this powerup grants the player invisibility for the next attack that hits them
    after this the shield dissapears."""

    def __init__(self):
        self.root_widget: FloatLayout | None = None
        self.shield = Image(source=shield_image, allow_stretch=True,
                            size_hint=(.05, .08), pos_hint={'x': .2075, 'y': .9125})
        self.shield_on_screen = False

    def draw_shield(self, root_widget: FloatLayout) -> None:
        """Draw the shield on screen"""

        self.root_widget = root_widget
        self.root_widget.add_widget(self.shield)
        self.shield_on_screen = True

    def remove_shield(self) -> None:
        """Remove the shield from screen"""

        music_client.play_shield_breaking_sfx()
        self.root_widget.remove_widget(self.shield)
        self.shield_on_screen = False


shield = Shield()
