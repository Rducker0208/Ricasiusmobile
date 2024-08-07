from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from start_screen import StartScreen
from game_screen import GameScreen
from game_over_screen import GameOverScreen

__version__ = '2.3.0'


class RicasiusApp(App):
    """Class that is used to initialise the app"""

    def __init__(self, **kwargs) -> None:
        super(RicasiusApp, self).__init__(**kwargs)

        # // Screen manager is used to switch between different screens
        self.sm = ScreenManager(transition=NoTransition())

    def build(self) -> ScreenManager:

        self.sm.add_widget(StartScreen(name='start'))
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(GameOverScreen(name='game_over'))

        self.sm.current = 'start'

        return self.sm


if __name__ == '__main__':
    RicasiusApp().run()
