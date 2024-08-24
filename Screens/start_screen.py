from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from user_class import user
from .leaderboard_screen import LeaderboardScreen
from .settings_screen import SetingsScreen

# // Images used
# // text acquired from: https://textcraft.net/
background_image = './Resources/start_screen/temple_bg.png'
highscore_text = './Resources/start_screen/highscore_text.png'
settings_image = './Resources/start_screen/cog.png'
trophy_image = './Resources/start_screen/trophy.png'
ricasius_text = './Resources/start_screen/ricasius.png'
battle_wz_text = './Resources/start_screen/battle_with_zeus.png'
press_to_start_text = './Resources/start_screen/press_to_start.png'

# // font
# // font acquired from: https://www.dafont.com/minecrafter.font
minecrafter_font = './Resources/fonts/Minecrafter.Reg.ttf'
LabelBase.register(name='minecraft', fn_regular=minecrafter_font)


class StartScreen(Screen):
    """Screen used to enter the game and display the user's highscore aswell as other options"""

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        # // Button to start the game
        self.start_game_button = Button(background_color=(0, 0, 0, 0))
        self.start_game_button.bind(on_press=self.start_game)

        # // Button to open the leaderboard
        self.leaderboard_button = Button(background_normal=trophy_image, background_down=trophy_image,
                                         size_hint=(.13, .25), pos_hint={'x': .745, 'y': .74})
        self.leaderboard_button.bind(on_press=self.open_leaderboard)

        # // Button to open the settings
        self.settings_menu_button = Button(background_normal=settings_image, background_down=settings_image,
                                           size_hint=(.13, .25), pos_hint={'x': .86, 'y': .74})
        self.settings_menu_button.bind(on_press=self.open_settings)

        self.add_widget(start_screen_widgets(self.leaderboard_button,
                                             self.start_game_button, self.settings_menu_button))


    def start_game(self, instance) -> None:  # noqa
        """Starts the main game"""

        self.manager.current = 'game'
        self.manager.remove_widget(self.manager.get_screen(name='start'))

    def open_settings(self, instance) -> None: # noqa
        """Opens the settings menu"""

        self.manager.add_widget(SetingsScreen(name='settings'))
        self.manager.current = 'settings'

    def open_leaderboard(self, instance) -> None: # noqa
        """Open the leaderboard menu"""

        self.manager.add_widget(LeaderboardScreen(name='leaderboard'))
        self.manager.current = 'leaderboard'


class start_screen_widgets(FloatLayout):
    """This layout contains all the graphical aspects of the widgets that are actually shown on this screen"""

    def __init__(self, leaderboard_button: Button, start_game_button: Button,  settings_button: Button, **kwargs) -> None:
        super(start_screen_widgets, self).__init__(**kwargs)

        self.add_widget(Image(source=background_image, allow_stretch=True, keep_ratio=False))

        # // Text displayed on screen
        self.add_widget(Image(source=highscore_text, allow_stretch=True,
                              size_hint=(.2, .1), pos_hint={'x': 0.03, 'y': .85}))

        self.add_widget(Label(text=str(user.highscore), font_name='minecraft', font_size=96,
                              outline_color=(255, 255, 255, 255), outline_width=4, color=(64, 75, 77, 1),
                              size_hint=(.2, .1), pos_hint={'x': 0.025, 'y': .75}))

        self.add_widget(Image(source=ricasius_text, allow_stretch=True,
                              size_hint=(.6, .25), pos_hint={'x': .2, 'y': .7}))

        self.add_widget(Image(source=battle_wz_text, allow_stretch=True,
                              size_hint=(.5, .15), pos_hint={'x': .25, 'y': .6}))

        self.add_widget(Image(source=press_to_start_text, allow_stretch=True,
                              size_hint=(.5, .15), pos_hint={'x': .24, 'y': .1}))

        # // Buttons to open other screens
        self.add_widget(start_game_button)
        self.add_widget(leaderboard_button)
        self.add_widget(settings_button)
