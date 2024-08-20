from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.image import Image

# // images used
zeus_image = r'./Resources/game_screen/zeus.png'


class Zeus:
    """Class that handles everything related to Zeus"""

    def __init__(self):
        self.zeus = Image(source=zeus_image, allow_stretch=True,
                          size_hint=(.15, .25),
                          x=Window.size[0] // 2 - Window.size[0] // 12,
                          y=Window.size[1] // 2 + Window.size[1] // 4.1)

        self.start_animation()

    def start_animation(self) -> None:
        """Start an animation loop for Zeus"""

        anim = (Animation(x=self.zeus.x + Window.size[0] // 16, y=self.zeus.y, duration=1.5) +
                Animation(x=self.zeus.x - Window.size[0] // 16, y=self.zeus.y, duration=1.5))
        anim.repeat = True
        anim.start(self.zeus)


zeus = Zeus()
