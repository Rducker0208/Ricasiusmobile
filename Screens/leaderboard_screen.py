import requests.exceptions

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from Entities import LeaderBoard

# // Images used
# // text acquired from: https://textcraft.net/
arrow_left = './Resources/settings_screen/arrow_to_left.png'
leaderboard_bg = './Resources/leaderboard_screen/leaderboard_bg.png'
leaderboard_text = './Resources/leaderboard_screen/Leaderboard.png'
no_connection = './Resources/leaderboard_screen/no_connection.png'
no_connection_text = './Resources/leaderboard_screen/no_connection_text.png'


class LeaderboardScreen(Screen):
    """
    Screen that displays a leaderboard containing names and scores of the 10 highest scorers.
    This screen has 2 styles:
    1: The standard leaderboard screen explained above.
    2: A screen displayed if the user has no active wifi connection
    """

    def __init__(self, **kw):
        super(LeaderboardScreen, self).__init__(**kw)

        # // button that goes back to log in screen
        last_page_button = Button(background_normal=arrow_left, background_down=arrow_left,
                                  size_hint=(.3, .4), pos_hint={'x': -.08, 'y': .68})
        last_page_button.bind(on_press=self.go_to_start)

        # // Check if user has Wi-Fi and choose which screen to display
        try:
            leaderboard = LeaderBoard()
            self.add_widget(LeaderBoardWidgets(last_page_button, True, leaderboard))
        except requests.exceptions.ConnectionError:
            self.add_widget(LeaderBoardWidgets(last_page_button, False, None))

    def go_to_start(self, instance) -> None:  # noqa
        """Go back to the start menu"""

        self.manager.current = 'start'
        self.manager.remove_widget(self.manager.get_screen(name='leaderboard'))


class LeaderBoardWidgets(FloatLayout):
    """This layout contains all the graphical aspects of the widgets that are actually shown on this screen"""

    def __init__(self, last_page_button: Button, user_has_internet: bool, leaderboard: LeaderBoard | None, **kwargs):

        super().__init__(**kwargs)

        # // Widgets that need to get added no matter what
        self.add_widget(Image(source=leaderboard_bg, allow_stretch=True, keep_ratio=False))
        self.add_widget(last_page_button)

        # // Check which screen to display, see the docstring for LeaderBoardScreen for more info
        if user_has_internet:

            self.add_widget(Image(source=leaderboard_text, allow_stretch=True,
                                  size_hint=(.6, .3), pos_hint={'x': .200, 'y': .75}))

            amount_of_players = len(leaderboard.top_ten['names'])

            # // Add at most 10 users
            for i in range(10):
                if amount_of_players > i:
                    self.add_widget(Label(text=f'{i + 1}.',
                                          size_hint=(.1, .08), pos_hint={'x': .3, 'y': -0.05 + .08 * (10 - i)}))
                    self.add_widget(Label(text=leaderboard.top_ten['names'][i],
                                          size_hint=(.1, .08), pos_hint={'x': .45, 'y': -0.05 + .08 * (10 - i)}))
                    self.add_widget(Label(text=str(leaderboard.top_ten['scores'][i]),
                                          size_hint=(.1, .08), pos_hint={'x': .6, 'y': -0.05 + .08 * (10 - i)}))

                else:
                    self.add_widget(Label(text=f'{i + 1}.',
                                          size_hint=(.1, .08), pos_hint={'x': .3, 'y': -0.05 + .08 * (10 - i)}))
                    self.add_widget(Label(text='-',
                                          size_hint=(.1, .08), pos_hint={'x': .45, 'y': -0.05 + .08 * (10 - i)}))
                    self.add_widget(Label(text='N/A',
                                          size_hint=(.1, .08), pos_hint={'x': .6, 'y': -0.05 + .08 * (10 - i)}))

        # // Widgets displayed if user is offline
        else:

            self.add_widget(Image(source=leaderboard_text, allow_stretch=True,
                                  size_hint=(.6, .3), pos_hint={'x': .200, 'y': .75}))

            self.add_widget(Image(source=no_connection, allow_stretch=True,
                                  size_hint=(.425, .425), pos_hint={'x': .3, 'y': .325}))

            self.add_widget(Image(source=no_connection_text, allow_stretch=True,
                                  size_hint=(.425, .2), pos_hint={'x': .31, 'y': .125}))




