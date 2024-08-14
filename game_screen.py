from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition, NoTransition

from attacks import AttackGrid
from database_class import db
from game_over_screen import GameOverScreen
from grape_class import grapes
from hp_class import hp
from joystick import Joystick
from music_client import music_client
from player_class import player
from user_class import user
from zeus_class import zeus

# // Images used
# // text acquired from: https://textcraft.net/
background_image = './Resources/game_screen/battle_background.png'
grape_image = './Resources/game_screen/grapes/grape_midle.png'


class GameScreen(Screen):
    """Class used to display the game itself"""

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.counter = 0

        widgets = game_screen_widgets()
        self.add_widget(widgets)

        # // check player hp and end game if player has no hp left
        Clock.schedule_interval(self.check_hp, 0.0333)

        # // update screen in 30 fps
        Clock.schedule_interval(widgets.update_screen, 0.033)

    def check_hp(self, dt) -> None: # noqa
        """Function that checks player's hp and stops game if player has no hp left"""

        # // Screen only needs to be updated if game is going on
        if self.manager.current == 'game':
            if player.hp <= 0:
                music_client.stop_main_theme()
                music_client.play_evil_laugh()

                # // Update highscore information and load appropriate game over screen
                self.manager.remove_widget(self.manager.get_screen(name='game_over'))

                if user.current_score > int(user.highscore):
                    user.highscore = user.current_score
                    db.update_user(user.username, user.highscore)
                    widgets = GameOverScreen(True, name='game_over')

                else:
                    widgets = GameOverScreen(False, name='game_over')

                self.manager.add_widget(widgets)
                self.manager.transition = FadeTransition()
                self.manager.current = 'game_over'
                self.manager.transition = NoTransition()
            #
            # if self.counter == 100:
            #     player.hp -= 1
            #     self.counter = 0
            # else:
            #     self.counter += 1


class game_screen_widgets(FloatLayout):
    """Class that contains all widgets used to display the game"""

    def __init__(self, **kwargs):
        super(game_screen_widgets, self).__init__(**kwargs)

        self.attack_grid = None
        self.attack_on_screen = False
        self.frames_since_last_attack = 0

        # // joystick used to register player movement
        joystick = Joystick(
            sticky=False,
            size_hint=(.4, .4),
            pos_hint={'x': -.1, 'y': .01}
        )
        joystick.bind(pad=get_joystick_input)

        # // grape image and score label to keep track of player score
        self.score_grape = Image(source=grape_image, allow_stretch=True,
                                 size_hint=(.07, .1), pos_hint={'x': -0.005, 'y': .81})

        self.score_label = Label(text=str(user.current_score), font_size=64, color='black',
                                 size_hint=(.1, .1), pos_hint={'x': .03, 'y': .81})

        # // add background
        self.add_widget(Image(source=background_image,
                              allow_stretch=True, keep_ratio=False))

        # // add all widgets created above and other classes
        self.add_widget(joystick)
        self.add_widget(self.score_grape)
        self.add_widget(self.score_label)
        self.add_widget(hp.hearts)
        self.add_widget(player.player)
        self.add_widget(zeus.zeus)

    def update_screen(self, dt) -> None: # noqa
        """Function that gets called every 1/30th of a second (dt) to update all widgets"""

        # // update player hp
        hp.update_hp(self)

        # // update label to show player their current score
        self.score_label.text = str(user.current_score)

        # // remove grapes if player is touching them and update player score
        grapes.update_grapes(self)

        # // update player location on screen
        player.update_player(self)

        # // update Zeus's position
        zeus.update_zeus(self)

        # // update attack
        if self.attack_on_screen is True:
            if self.attack_grid.status == 'finished':
                self.attack_on_screen = False
                self.frames_since_last_attack = 0

        else:
            if self.frames_since_last_attack == 100:
                self.attack_grid = AttackGrid()
                self.add_widget(self.attack_grid)
                self.attack_on_screen = True

            else:
                self.frames_since_last_attack += 1

        # # // update attack
        # if self.frames_since_attack_change == 100:
        #     if self.attack_on_screen is True:
        #         ...
        #
        #     else:
        #         self.attack_grid = AttackGrid()
        #         self.add_widget(self.attack_grid)
        #         self.attack_on_screen = True
        #
        #     self.frames_since_attack_change = 0
        #
        # else:
        #     if self.attack_on_screen is True:
        #         self.attack_grid.update_attack()
        #
        #     self.frames_since_attack_change += 1
        #
        # if self.attack_on_screen:
        #     self.attack_grid.update_attack_circles()
        #
        # elif self.frames_since_attack_change == 100:
        #     self.attack_grid = AttackGrid()
        #     self.add_widget(self.attack_grid)
        #     self.attack_on_screen = True
        #
        # else:
        #     self.frames_since_attack_change += 1
        # #
        # # // Update attack
        # if self.frames_since_attack_change == 100:
        #     self.frames_since_attack_change = 0
        #     if self.attack_on_screen is False:

        #     else:
        #         self.remove_widget(self.attack_grid)
        #         self.attack_on_screen = False
        # else:
        #     self.frames_since_attack_change += 1



def get_joystick_input(joystick, pad) -> None: # noqa
    """Function to track current position of joystick to get player movement"""

    # // pad[0] = x_axis
    # // pad[1] = y_axis
    x_direction, y_direction = pad

    # // see if joystick is held to left or to the right
    if x_direction > 0:
        player.x_axis = 'right'
    elif x_direction < 0:
        player.x_axis = 'left'
    else:
        player.x_axis = None

    # // see if joystick is held up or down
    if y_direction > 0:
        player.y_axis = 'up'
    elif y_direction < 0:
        player.y_axis = 'down'
    else:
        player.y_axis = None

    # // set player speed in relation to joystick position
    player.speed_x = round(x_direction, 2)
    player.speed_y = round(y_direction, 2)

