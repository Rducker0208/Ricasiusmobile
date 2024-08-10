from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from music_client import music_client

# // images used
# // text acquired from: https://textcraft.net/
background_image = './Resources/game_over_screen/temple_bg.png'
you_died_text = './Resources/game_over_screen/you_died.png'
press_to_respawn = './Resources/game_over_screen/press_to_respawn.png'


class GameOverScreen(Screen):
    """Class that handles the screen displayed on death of the player"""

    def __init__(self, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)

        self.restart_game_button = Button(background_color=(0, 0, 0, 0))
        self.restart_game_button.bind(on_press=self.restart_game)

        self.add_widget(game_over_screen_widgets(self.restart_game_button))


    def restart_game(self, instance) -> None: # noqa
        music_client.play_main_theme()
        self.manager.current = 'start'


class game_over_screen_widgets(FloatLayout):
    """Class containing all widgets for game over screen"""

    def __init__(self, restart_game_button: Button, **kwargs):
        super(game_over_screen_widgets, self).__init__(**kwargs)

        self.restart_game_button = restart_game_button

        self.add_widget(Image(source=background_image, allow_stretch=True, keep_ratio=False))

        self.add_widget(Image(source=you_died_text, allow_stretch=True,
                              size_hint=(.6, .2), pos_hint={'x': .2, 'y': .75}))

        self.add_widget(Image(source=press_to_respawn, allow_stretch=True,
                              size_hint=(.5, .15), pos_hint={'x': .26, 'y': .1}))

        self.add_widget(self.restart_game_button)



