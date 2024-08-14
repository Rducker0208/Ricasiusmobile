import random

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

# // images used
red_circle = './Resources/game_screen/attacks/red_circle.png'
red_cross = './Resources/game_screen/attacks/red_cross.png'


class AttackGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 15
        self.rows = 9

        self.status = 'pre_lightning'
        self.lightning = Lightning()

        self.attack_locations = choose_attack_locations()
        self.attack_circles = []
        self.opacity_direction = 'down'

        self.draw_attack_circles()

    def draw_attack_circles(self) -> None:
        """Draw a grid of future attack locations marked by a red circle"""

        for i in range(1, 106):
            if i in self.attack_locations:
                attack_circle = Image(source=red_circle, allow_stretch=True, keep_ratio=False)
                self.add_widget(attack_circle)
                self.attack_circles.append(attack_circle)
            else:
                self.add_widget(Button(background_color=(0, 0, 0, 1), disabled=True))

    def update_attack(self) -> None:
        """Update attack circles or lightning depending on attack status"""

        # // if the red warning circles are still on screen
        if self.status == 'pre_lightning':

            # // check if opacity is going down or up
            if self.opacity_direction == 'down':
                for image in self.attack_circles:
                    image.opacity -= .03

                if self.attack_circles[0].opacity < 0:
                    self.opacity_direction = 'up'

            else:
                for image in self.attack_circles:
                    image.opacity += .03

                # // if animation of the red circles fading is finished,
                # // remove them from the screen and start the lightning
                if self.attack_circles[0].opacity == 1:
                    self.clear_widgets()
                    self.status = 'during_lightning'

        elif self.status == 'during_lightning':
            ...


def choose_attack_locations() -> list:
    """Chooses attack locations"""

    locations = []

    for i in range(52):
        while True:
            new_location = random.randint(31, 106)
            if new_location in [61, 62, 63, 76, 77, 78, 91, 92, 93]:
                continue
            else:
                break
        locations.append(new_location)

    return locations


class Lightning:
    def __init__(self):
        ...

    def update_lightning(self):
        ...