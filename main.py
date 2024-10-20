import kivy

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from Screens import LoginScreen, StartScreen, GameScreen
from user_class import user

try:
    from music_client import music_client
except:
    user.user_has_speakers = False

kivy.require('2.3.0')


class RicasiusApp(App):
    """Class that is used to initialise the app"""

    def __init__(self, **kwargs) -> None:
        super(RicasiusApp, self).__init__(**kwargs)

        # // Screen manager is used to switch between different screens
        self.sm = ScreenManager(transition=NoTransition())

    def build(self) -> ScreenManager:
        """Build the screenmanager and initialise the app"""

        self.sm.add_widget(GameScreen(name='game'))

        # // Check if user should log in
        if not user.username:
            self.sm.add_widget(LoginScreen(name='login'))
            self.sm.current = 'login'
        else:
            music_client.play_main_theme()
            self.sm.add_widget(StartScreen(name='start'))
            self.sm.add_widget(LoginScreen(name='login'))
            self.sm.current = 'start'

        return self.sm


if __name__ == '__main__':
    RicasiusApp().run()
