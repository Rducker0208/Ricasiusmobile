import requests.exceptions
from kivy.uix.button import Button
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
    """Class used to display the leaderboard"""

    def __init__(self, **kw):
        super(LeaderboardScreen, self).__init__(**kw)

        try:
            leaderboard = LeaderBoard()

            self.add_widget(Image(source=leaderboard_bg, allow_stretch=True, keep_ratio=False))

            # // button that goes back to log in screen
            last_page_button = Button(background_normal=arrow_left, background_down=arrow_left,
                                      size_hint=(.3, .4), pos_hint={'x': -.08, 'y': .68})
            last_page_button.bind(on_press=self.go_to_start)
            self.add_widget(last_page_button)

            self.add_widget(Image(source=leaderboard_text, allow_stretch=True,
                                  size_hint=(.6, .3), pos_hint={'x': .200, 'y': .75}))

            amount_of_players = len(leaderboard.top_ten['names'])
            print(amount_of_players)

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

        except requests.exceptions.ConnectionError:
            self.add_widget(Image(source=leaderboard_bg, allow_stretch=True, keep_ratio=False))

            # // button that goes back to log in screen
            last_page_button = Button(background_normal=arrow_left, background_down=arrow_left,
                                      size_hint=(.3, .4), pos_hint={'x': -.08, 'y': .68})
            last_page_button.bind(on_press=self.go_to_start)
            self.add_widget(last_page_button)

            self.add_widget(Image(source=leaderboard_text, allow_stretch=True,
                                  size_hint=(.6, .3), pos_hint={'x': .200, 'y': .75}))

            self.add_widget(Image(source=no_connection, allow_stretch=True,
                                  size_hint=(.425, .425), pos_hint={'x': .3, 'y': .325}))

            self.add_widget(Image(source=no_connection_text, allow_stretch=True,
                                  size_hint=(.425, .2), pos_hint={'x': .31, 'y': .125}))

    def go_to_start(self, instance) -> None:  # noqa
        """Go back to the start menu"""

        self.manager.current = 'start'
        self.manager.remove_widget(self.manager.get_screen(name='leaderboard'))


