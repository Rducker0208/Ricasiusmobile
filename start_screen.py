from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from database_class import database
from user_class import User


# // Images used
# // text acquired from: https://textcraft.net/
background_image = './Resources/start_screen/temple_bg.png'
highscore_text = './Resources/start_screen/highscore_text.png'
highscore = './Resources/start_screen/highscore.png'
ricasius_text = './Resources/start_screen/ricasius.png'
battle_wz_text = './Resources/start_screen/battle_with_zeus.png'
press_to_start_text = './Resources/start_screen/press_to_start.png'


class StartScreen(Screen):
    """Class used to display the startscreen"""

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.user = User()

        self.start_game_button = Button(background_color=(0, 0, 0, 0))
        self.start_game_button.bind(on_press=self.start_game)

        self.add_widget(start_screen_widgets(self.start_game_button, self.user))

    def start_game(self, instance) -> None: # noqa
        self.manager.current = 'game'


class start_screen_widgets(FloatLayout):
    """Class that contains all widgets for the startscreen"""

    def __init__(self, start_game_button: Button, user: User, **kwargs) -> None:
        super(start_screen_widgets, self).__init__(**kwargs)

        self.start_game_button = start_game_button
        self.user = user
        self.highscore = database(self.user.username).load_user()

        self.user.create_score_image(mode='highscore')

        self.add_widget(Image(source=background_image, allow_stretch=True, keep_ratio=False))

        self.add_widget(Image(source=highscore_text, allow_stretch=True,
                              size_hint=(.2, .1), pos_hint={'x': 0.03, 'y': .85}))

        self.add_widget(Image(source=highscore, allow_stretch=True,
                              size_hint=(.2, .1), pos_hint={'x': 0.022, 'y': .77}))

        self.add_widget(Image(source=ricasius_text, allow_stretch=True,
                              size_hint=(.6, .25), pos_hint={'x': .2, 'y': .7}))

        self.add_widget(Image(source=battle_wz_text, allow_stretch=True,
                              size_hint=(.5, .15), pos_hint={'x': .25, 'y': .6}))

        self.add_widget(Image(source=press_to_start_text, allow_stretch=True,
                              size_hint=(.5, .15), pos_hint={'x': .24, 'y': .1}))

        self.add_widget(self.start_game_button)
