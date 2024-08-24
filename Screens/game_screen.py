import random
import requests.exceptions

from jnius import autoclass
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import FadeTransition, NoTransition, Screen

from database_class import db
from Entities import attack, grapes, hp, LeaderBoard, LootVase, player, shield, speed_boots, zeus
from joystick import Joystick
from music_client import music_client
from user_class import user
from .game_over_screen import GameOverScreen


# // Images used
# // text acquired from: https://textcraft.net/
background_image = './Resources/game_screen/new_map_3.png'
grape_image = './Resources/game_screen/grapes/grape_middle.png'


class GameScreen(Screen):
    """Class that displays the screen used in the actual battle with Zeus"""

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.widgets = game_screen_widgets()
        self.add_widget(self.widgets)

        # // check player hp and end game if player has no hp left
        Clock.schedule_interval(self.update_screen, 0.0333)

    def update_screen(self, dt) -> None:  # noqa
        """Function that checks player's hp and stops the game if player has no hp left"""

        # // Screen only needs to be updated if game is going on
        if self.manager.current == 'game':
            self.widgets.update_screen()

            if player.hp <= 0:
                music_client.stop_main_theme(True, 0.0)

                # // Update highscore information and load appropriate game over screen
                if user.current_score > int(user.highscore):
                    new_hs = True
                    user.highscore = user.current_score
                    db.update_user_score(user.username, user.highscore)
                    game_over_widgets = GameOverScreen(True, name='game_over')

                else:
                    new_hs = False
                    game_over_widgets = GameOverScreen(False, name='game_over')

                # // Try vibrating the current device,
                # // if the current device does not posess a vibrator pass this code
                if user.user_settings['vibrations_on'] is True:
                    try:
                        PythonActivity = autoclass('org.kivy.android.PythonActivity')
                        Context = autoclass('android.content.Context')
                        activity = PythonActivity.mActivity
                        vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
                        vibrator.vibrate(500)

                    except Exception as e:
                        if 'org/kivy/android/PythonActivity java.lang.NoClassDefFoundError' in str(e):
                            pass
                        else:
                            print(e)

                # // Add the game over screen to the screenmanager and switch to it
                self.manager.add_widget(game_over_widgets)
                self.manager.transition = FadeTransition()
                self.manager.current = 'game_over'
                self.manager.transition = NoTransition()

                # // This is done later so that the transition doesn't take long to start
                if new_hs:
                    try:
                        LeaderBoard().update_leaderboard(user.username, user.current_score)
                    except requests.exceptions.ConnectionError:
                        pass


class game_screen_widgets(FloatLayout):
    """This layout contains all the graphical aspects of the widgets that are actually shown on this screen"""

    def __init__(self, **kwargs):
        super(game_screen_widgets, self).__init__(**kwargs)

        # // Variables used for controling powerups
        self.loot_vase = None
        self.power_up = None
        self.vase_on_screen = False
        self.power_up_on_screen = False

        # // Variables used for controling attacks
        self.attack_on_screen = False
        self.frames_since_last_attack = 0

        # // Joystick used to register player movement
        joystick = Joystick(
            sticky=False,
            size_hint=(.4, .4),
            pos_hint={'x': -.1, 'y': .01}
        )
        joystick.bind(pad=get_joystick_input)

        # // Grape image and score label to keep track of player score
        self.score_grape = Image(source=grape_image, allow_stretch=True,
                                 size_hint=(.07, .1), pos_hint={'x': -0.005, 'y': .81})

        self.score_label = Label(text=str(user.current_score), font_size=64, color='black',
                                 size_hint=(.1, .1), pos_hint={'x': .03, 'y': .81})

        # // Add background
        self.add_widget(Image(source=background_image,
                              allow_stretch=True, keep_ratio=False))

        # // Add all widgets that are created above, also add all the remaining classes
        self.add_widget(joystick)
        self.add_widget(self.score_grape)
        self.add_widget(self.score_label)
        self.add_widget(hp.hearts)
        self.add_widget(player.player)
        self.add_widget(zeus.zeus)

    def update_screen(self) -> None:  # noqa
        """Function that gets called every 1/30th of a second to update all widgets"""

        # // Update player hp
        hp.update_hp(self)

        # // Update label to show player their current score
        self.score_label.text = str(user.current_score)

        # // Remove grapes if player is touching them and update player score
        grapes.update_grapes(self)

        # // Update player location on screen
        player.update_player(self)

        # // Update attack
        if self.attack_on_screen is True:
            if attack.finished is True:
                self.remove_widget(attack)
                self.attack_on_screen = False
                self.frames_since_last_attack = 0

        else:
            if self.frames_since_last_attack == 50:
                self.add_widget(attack)
                self.attack_on_screen = True
                attack.draw_attack_circles(1, 6, 0.0)
                attack.finished = False

            else:
                self.frames_since_last_attack += 1
                attack.add_attack_location()

        # // Update vase
        # // Check if there should be a loot vase spawned
        if self.vase_on_screen is False and self.power_up_on_screen is False:
            if random.randint(1, 1000) == 1:
                self.loot_vase = LootVase(self)
                self.vase_on_screen = True

        # // If there is a vase on screen, check for colision
        if self.vase_on_screen is True:
            if self.loot_vase.check_colision():
                self.vase_on_screen = False

                # // Randomly choose which power up should be spawned
                if random.randint(1, 2) == 1:
                    shield.draw_shield(self)
                    self.power_up = 'shield'
                else:
                    speed_boots.draw_boots(self)
                    speed_boots.active = True
                    self.power_up = 'speed_boots'
                self.power_up_on_screen = True

        # // Update powerup
        if shield.shield_on_screen is False and self.power_up_on_screen is True:

            # // This condition gets triggered if the player loses hp and the shield is removed in the attack class
            if self.power_up == 'shield':
                self.power_up_on_screen = False

            # // This condition gets triggered if the speed bots have run out
            elif speed_boots.active is False:
                self.power_up_on_screen = False


def get_joystick_input(joystick, pad) -> None:  # noqa
    """Function to track current position of joystick to control player movement"""

    # // pad[0] = x_axis
    # // pad[1] = y_axis
    x_direction, y_direction = pad

    # // Check if joystick is held to left or to the right
    if x_direction > 0:
        player.x_axis = 'right'
    elif x_direction < 0:
        player.x_axis = 'left'

    # // Check if joystick is held up or down
    if y_direction > 0:
        player.y_axis = 'up'
    elif y_direction < 0:
        player.y_axis = 'down'
    else:
        player.y_axis = None

    # // Set player speed based on how far the joystick is from the center of its platform
    player.speed_x = round(x_direction, 2)
    player.speed_y = round(y_direction, 2)
