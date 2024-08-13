import kivy

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from game_over_screen import GameOverScreen
from game_screen import GameScreen
from login_screen import LoginScreen
from start_screen import StartScreen
from user_class import user

kivy.require('2.3.0')


class RicasiusApp(App):
    """Class that is used to initialise the app"""

    def __init__(self, **kwargs) -> None:
        super(RicasiusApp, self).__init__(**kwargs)

        # // Screen manager is used to switch between different screens
        self.sm = ScreenManager(transition=NoTransition())

    def build(self) -> ScreenManager:
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(GameOverScreen(False, name='game_over'))

        # // Check if user should log in
        if not user.username:
            print('1')
            self.sm.add_widget(LoginScreen(name='login'))
            self.sm.current = 'login'
        else:
            print('2')
            user.create_score_image(mode='highscore')
            self.sm.add_widget(StartScreen(name='start'))
            self.sm.current = 'start'

        return self.sm


if __name__ == '__main__':
    RicasiusApp().run()
