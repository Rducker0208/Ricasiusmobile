from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from grape_class import Grapes
from hp_class import hp
from joystick import Joystick
from player_class import Player
from user_class import User
from zeus_class import Zeus

# // Images used
# // text acquired from: https://textcraft.net/
background_image = './Resources/game_screen/battle_background.png'
grape_image = './Resources/game_screen/grape.png'
# Clock.max_iteration = 500


class GameScreen(Screen):
    """Class used to display the game itself"""

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.player = Player()
        self.counter = 0

        widgets = game_screen_widgets(self.player)
        self.add_widget(widgets)

        # // check player hp and end game if player has no hp left
        Clock.schedule_interval(self.check_hp, 0.0333)

        # // update screen in 30 fps
        Clock.schedule_interval(widgets.update_screen, 0.033)

    def check_hp(self, dt) -> None: # noqa
        """Function that checks player's hp and stops game if player has no hp left"""

        if self.player.hp <= 0:
            self.manager.current = 'game_over'
        #
        # if self.counter == 50:
        #     print('p')
        #     self.player.hp -= 1
        #     self.counter = 0
        # else:
        #     self.counter += 1


class game_screen_widgets(FloatLayout):
    """Class that contains all widgets used to display the game"""

    def __init__(self, player, **kwargs):
        super(game_screen_widgets, self).__init__(**kwargs)

        # // initialize classes used to control game flow
        self.player = player
        self.grapes = Grapes()
        self.hp = hp()
        self.user = User()
        self.zeus = Zeus()

        # // joystick used to register player movement
        joystick = Joystick(
            sticky=False,
            size_hint=(.25, .25),
            pos_hint={'x': -.05, 'y': .05}
        )
        joystick.bind(pad=self.get_joystick_input)

        # // grape image and score label to keep track of player score
        self.score_grape = Image(source=grape_image, allow_stretch=True,
                                 size_hint=(.1, .1), pos_hint={'x': .9, 'y': .885})

        self.score_label = Label(text=str(self.user.current_score), font_size=64, color='black',
                                 size_hint=(.1, .1), pos_hint={'x': .82, 'y': .88})

        # // add background
        self.add_widget(Image(source=background_image,
                              allow_stretch=True, keep_ratio=False))

        # // add all widgets created above
        self.add_widget(joystick)
        self.add_widget(self.score_grape)
        self.add_widget(self.score_label)
        self.add_widget(self.hp.hearts)
        self.add_widget(self.player.player)
        self.add_widget(self.zeus.zeus)

    def update_screen(self, dt) -> None: # noqa
        """Function that gets called every 1/30th of a second (dt) to update all widgets"""

        # // update player hp
        self.hp.update_hp(self, self.player)

        # // update label to show player their current score
        self.score_label.text = str(self.user.current_score)

        # // remove grapes if player is touching them and update player score
        self.grapes.update_grapes(self, self.player, self.user)

        # // update player location on screen
        self.player.update_player(self)

        # // update Zeus's position
        self.zeus.update_zeus(self)


    def get_joystick_input(self, joystick, pad) -> None: # noqa
        """Function to track current position of joystick to get player movement"""

        # // pad[0] = x_axis
        # // pad[1] = y_axis
        x_direction, y_direction = pad

        # // see if joystick is held to left or to the right
        if x_direction > 0:
            self.player.x_axis = 'right'
        elif x_direction < 0:
            self.player.x_axis = 'left'
        else:
            self.player.x_axis = None

        # // see if joystick is held up or down
        if y_direction > 0:
            self.player.y_axis = 'up'
        elif y_direction < 0:
            self.player.y_axis = 'down'
        else:
            self.player.y_axis = None

        # // set player speed in relation to joystick position
        self.player.speed_x = round(x_direction, 2)
        self.player.speed_y = round(y_direction, 2)
