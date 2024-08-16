import random

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from jnius import autoclass
from music_client import music_client
from .player_class import player

# // images used
red_circle = './Resources/game_screen/attacks/red_circle.png'
red_cross = './Resources/game_screen/attacks/red_cross.png'
lightning_dir = '../Resources/game_screen/lightning/'

joystick_area = [60, 61, 62, 63, 75, 76, 77, 78, 90, 91, 92, 93]


class AttackGrid(GridLayout):
    """Class that creates a grid with labals and red circles indicating incoming lightning bolts"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 15
        self.rows = 9

        self.status = 'pre_lightning'

        # // variables for attack grid
        self.attack_locations = choose_attack_locations()
        self.attack_circles = []
        self.opacity_direction = 'down'

        # // variables for lightning attack
        self.frames_since_lightning_update = 0
        self.lightning_animation_frame = 1
        self.lightning_bolts = []

        self.draw_attack_circles()

    def draw_attack_circles(self) -> None:
        """Draw a grid of future attack locations marked by a red circle"""

        for i in range(105):
            if i in self.attack_locations:
                attack_circle = Image(source=red_circle, allow_stretch=True, keep_ratio=False)
                self.add_widget(attack_circle)
                self.attack_circles.append(attack_circle)
            else:
                self.add_widget(Label())

    def draw_lightning(self) -> None:
        """Updates lightning on screen"""

        for i in range(0, 105):
            if i in self.attack_locations:
                lightning_bolt = Image(source=f'{lightning_dir}lightning_frame'
                                              f'_{self.lightning_animation_frame}.png',
                                       allow_stretch=True, keep_ratio=False)
                self.add_widget(lightning_bolt)
                self.lightning_bolts.append(lightning_bolt)

            # // A label doesn't hinder touching the joystick
            elif i in joystick_area:
                self.add_widget(Label())
            else:
                self.add_widget(Button(background_color=(0, 0, 0, 0), disabled=True))

        Clock.schedule_once(self.check_for_player_damage)

    def check_for_player_damage(self, instance) -> None:  # noqa
        """Check if the player is standing in any lightning bolts, if yes subtract 1 from the player's hp"""

        player_tile_x = player.player.x // (Window.size[0] / 15) + 1
        player_tile_y = player.player.y // (Window.size[1] / 9)

        if player_tile_y > 0:
            player_tile = 105 - player_tile_y * 15
        else:
            player_tile = 105
        player_tile -= (15 - player_tile_x)

        if player_tile in self.attack_locations:
            player.hp -= 5

            try:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                activity = PythonActivity.mActivity
                vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
                vibrator.vibrate(200)

            except Exception as e:
                print(e)

            return

    def update_attack_animation(self) -> None:
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
                    self.draw_lightning()
                    music_client.play_thunder_sfx()
                    self.status = 'during_lightning'

        elif self.status == 'during_lightning':

            # // check if lightning animation frame should be updated
            if self.frames_since_lightning_update == 10:

                # // update to the next animation frame and end the attack if needed
                self.lightning_animation_frame += 1
                if self.lightning_animation_frame == 8:
                    self.clear_widgets()
                    self.status = 'finished'
                    return

                # // update every lightning bolt
                for image in self.lightning_bolts:
                    image.source = (f'{lightning_dir}lightning_frame_'
                                    f'{self.lightning_animation_frame}.png')

                self.frames_since_lightning_update = 0

            else:
                self.frames_since_lightning_update += 1


def choose_attack_locations() -> list:
    """Chooses attack locations"""

    locations = []

    for i in range(26):

        # // Make sure attacks don't spawn in joystick
        while True:
            new_location = random.randint(31, 106)
            if new_location in joystick_area:
                continue
            else:
                break
        locations.append(new_location)

    return locations