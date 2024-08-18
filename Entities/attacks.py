import random

from functools import partial
from jnius import autoclass
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

from music_client import music_client
from user_class import user
from .player_class import player

# // images used
transparent_image = './Resources/game_screen/attacks/transparent_image.png'
red_circle = './Resources/game_screen/attacks/red_circle.png'
red_cross = './Resources/game_screen/attacks/red_cross.png'
lightning_dir = '../Resources/game_screen/lightning/'

blacklisted_tiles = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                     26, 27, 28, 29, 30, 76, 77, 78, 79, 91, 92, 93, 94, 106, 107, 108, 109, 121, 122, 123, 124}


class AttackGrid(GridLayout):
    """Class that creates a grid with labals and red circles indicating incoming lightning bolts"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 15
        self.rows = 9
        self.orientation = 'lr-tb'

        self.finished = False

        # // variables for attack grid
        self.attack_locations = set()

        # // variables for attack circles
        self.circle_opacity = 0

        # // variables for lightning attack
        self.lightning_animation_frame = 1

        self.create_attack_grid()


    def create_attack_grid(self) -> None: # noqa
        """Create a 15x9 grid on which attacks can take place"""

        # // This grid gets created at the start of the app to avoid lag later on
        for i in range(1, 136):
            self.add_widget(Image(source=transparent_image))

    def draw_attack_circles(self, first_circle: int, last_circle: int, dt: int) -> None: # noqa
        """Draw a grid of future attack locations marked by a red circle"""

        # // loop through 5 locations (not 15 to avoid lag) and place a red circle if needed
        for location in range(first_circle, last_circle):
            if location in self.attack_locations:
                self.children[-location].source = red_circle

            # // opacity 0 = transparent
            self.children[-location].opacity = 0

        # // Keep going until all 9 rows are covered
        if last_circle != 136:
            Clock.schedule_once(partial(self.draw_attack_circles, first_circle + 5, last_circle + 5), 0)
        else:
            Clock.schedule_once(partial(self.update_attack_opacity, 1, 16), 0)

    def update_attack_opacity(self, first_circle: int, last_circle: int, dt: int) -> None: # noqa
        """Lower the opacity of the attack circles in a certain row to give an effect of iminent danger"""

        # // loop through 5 locations (not 15 to avoid lag) and increase image opacity
        for i in range(first_circle, last_circle):
            self.children[-i].opacity += .03

        # // Keep continuing until the images are fully transparent
        if last_circle != 136:
            Clock.schedule_once(partial(self.update_attack_opacity, first_circle + 15, last_circle + 15))

        # // If maximum opacity is reached on the bottom rows the lightning can start
        elif self.children[-135].opacity >= 1:
            Clock.schedule_once(partial(self.draw_lightning, 1, 16, 1), 0)
        else:
            Clock.schedule_once(partial(self.update_attack_opacity, 1, 16), 0)

    def draw_lightning(self, first_circle: int, last_circle: int, animation_frame: int, dt: int) -> None: # noqa
        """Replace red circle with lightning"""

        # // Loop over every attack location and replace the source with the appropriate lightning frame
        for i in range(first_circle, last_circle):
            if i in self.attack_locations:
                self.children[-i].source = f'{lightning_dir}/lightning_frame_{animation_frame}.png'

        # // if the animation is on the final row and on the final animation then stop the attack
        if last_circle == 136:
            if animation_frame == 7:
                Clock.schedule_once(partial(self.clear_red_circles, 1, 6), 0.3)
            else:
                animation_frame += 1
                Clock.schedule_once(partial(self.draw_lightning, 1, 16, animation_frame), 0.2)

        # // Go through all the locations again to update to the next sprite
        else:

            # // If the lightning is on the first strike, check if the player should take damage and play the lightning
            # sound effect
            if animation_frame == 1:
                Clock.schedule_once(partial(self.check_for_player_damage, first_circle, last_circle), 0)

                if first_circle == 1:
                    music_client.play_thunder_sfx()

            Clock.schedule_once(partial(self.draw_lightning, first_circle + 15, last_circle + 15,
                                        animation_frame), 0)

    def check_for_player_damage(self, first_location: int, last_location: int, dt: int) -> None:  # noqa
        """Check if the player is standing in any lightning bolts, if yes subtract 1 from the player's hp"""

        # // Get (x, y) cords of player in relation to the parent gridlayout
        player_size_x, player_size_y = player.player.size
        player_tile_x = (player.player.x + player_size_x / 2) // (Window.size[0] / 15)
        player_tile_y = (player.player.y + player_size_y / 2) // (Window.size[1] / 9)

        player_tile = ((8 - player_tile_y) * 15) + player_tile_x + 1

        # // No need to check if the player is not in the current row
        if first_location <= player_tile <= last_location:

            # // Go through every location in the row to check if player is standing there
            for location in range(first_location, last_location + 1):
                if player_tile == location and location in self.attack_locations:
                    player.hp -= 1

                    if user.user_settings['vibrations_on'] is True:
                        try:
                            PythonActivity = autoclass('org.kivy.android.PythonActivity')
                            Context = autoclass('android.content.Context')
                            activity = PythonActivity.mActivity
                            vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
                            vibrator.vibrate(200)

                        except Exception as e:
                            if 'org/kivy/android/PythonActivity java.lang.NoClassDefFoundError' in str(e):
                                pass
                            else:
                                print(e)

    def clear_red_circles(self, first_circle: int, last_circle: int, dt: int): # noqa
        """Clear red circles from screen"""

        # // Clear all red circles in the row
        for location in range(first_circle, last_circle):
            if location in self.attack_locations:
                self.children[-location].source = transparent_image

        # // Go to the next row
        if last_circle != 136:
            Clock.schedule_once(partial(self.clear_red_circles, first_circle + 5, last_circle + 5), 0)

        # // If clean up is done reset variables needed for the next attack
        else:
            self.attack_locations = set()
            self.circle_opacity = 0
            self.lightning_animation_frame = 1
            self.finished = True

    def add_attack_location(self) -> None:
        """Add a new attack location every frame to avoid lag spikes"""

        for i in range(3):
            new_location = random.randint(1, 135)

            # // Make sure attacks do not spawn in joystick or out of bounds
            if new_location in blacklisted_tiles or new_location in self.attack_locations:
                continue
            else:
                self.attack_locations.add(new_location)
                break


attack = AttackGrid()
