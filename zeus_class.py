from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen


# // images used
zeus_image = r'./Resources/game_screen/zeus.png'


class Zeus:
    """Class that handles everything related to Zeus"""

    def __init__(self):
        self.zeus = Image(source=zeus_image, allow_stretch=True,
                          size_hint=(.2, .3),
                          x=Window.size[0] // 2 - Window.size[0] // 10,
                          y=Window.size[1] // 2 + Window.size[1] // 4.5)

        # // variables used for graphical purposes
        self.animation_duration = 0
        self.animation_direction = 'right'
        self.frames_since_animation = 0

    def update_zeus(self, screen: Screen) -> None:
        """Update Zeus's location on screen"""

        screen.remove_widget(self.zeus)

        if self.frames_since_animation == 3:

            if self.animation_direction == 'right':

                if self.animation_duration < 10:
                    self.zeus.x += Window.size[0] // 1000
                    self.animation_duration += 1

                else:
                    self.animation_direction = 'left'
                    self.animation_duration = 0

            else:
                if self.animation_duration < 10:
                    self.zeus.x -= Window.size[0] // 1000
                    self.animation_duration += 1

                else:
                    self.animation_direction = 'right'
                    self.animation_duration = 0

            self.frames_since_animation = 0

        else:
            self.frames_since_animation += 1

        screen.add_widget(self.zeus)


zeus = Zeus()
