from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from Entities import player

from music_client import music_client
from user_class import user
from .start_screen import StartScreen


# // images used
# // text acquired from: https://textcraft.net/
background_image = './Resources/game_over_screen/temple_bg.png'
you_died_text = './Resources/game_over_screen/You-died.png'
new_highscore_text = './Resources/game_over_screen/new-highscore.png'
highscore_text = './Resources/game_over_screen/highscore_text.png'
score_text = './Resources/game_over_screen/score_text.png'
press_to_respawn_text = './Resources/game_over_screen/press_to_respawn.png'

# // font
# // font acquired from: https://www.dafont.com/minecrafter.font
minecrafter_font = './Resources/fonts/Minecrafter.Reg.ttf'
LabelBase.register(name='minecraft', fn_regular=minecrafter_font)


class GameOverScreen(Screen):
    """
    Screen that is displayed upon the death of the player, this screen features 2 styles:
    1: A new highscore was reached
    2: The user did not surpass their previous record
    """

    def __init__(self, new_highscore: bool, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)

        # // Button used to restart the game
        self.restart_game_button = Button(background_color=(0, 0, 0, 0))
        self.restart_game_button.bind(on_press=self.restart_game)

        self.add_widget(game_over_screen_widgets(new_highscore, self.restart_game_button))


    def restart_game(self, instance) -> None: # noqa
        """Function that restarts the game, this function also sets all the variables that need to be reset
         so the game can function on reset"""

        # // Reset needed variables
        music_client.play_main_theme()
        user.current_score = 0
        player.hp = 5

        # // Add the start screen back to the screenmanager,
        # // this resets the widgets on the start screen so the highscore is refreshed
        self.manager.add_widget(StartScreen(name='start'))
        self.manager.current = 'start'
        self.manager.remove_widget(self.manager.get_screen(name='game_over'))


class game_over_screen_widgets(FloatLayout):
    """This layout contains all the graphical aspects of the widgets that are actually shown on this screen"""

    def __init__(self, new_highscore: bool, restart_game_button: Button, **kwargs):
        super(game_over_screen_widgets, self).__init__(**kwargs)

        self.restart_game_button = restart_game_button

        self.add_widget(Image(source=background_image, allow_stretch=True, keep_ratio=False))

        self.add_widget(Image(source=you_died_text, allow_stretch=True,
                              size_hint=(.6, .2), pos_hint={'x': .2, 'y': .75}))

        self.add_widget(Image(source=press_to_respawn_text, allow_stretch=True,
                              size_hint=(.5, .15), pos_hint={'x': .25, 'y': .001}))

        self.add_widget(self.restart_game_button)

        # // check which screen to display, see the styles in the docstring of the GameOverScreen class
        if new_highscore:
            self.add_widget(Image(source=new_highscore_text, allow_stretch=True,
                                  size_hint=(.4, .15), pos_hint={'x': .3, 'y': .6}))

            self.add_widget(Label(text=str(user.highscore), font_name='minecraft', font_size=256,
                                  outline_color=(255, 255, 255, 255), outline_width=4, color=(64, 75, 77, 1),
                                  size_hint=(.8, .2), pos_hint={'x': 0.1, 'y': .3}))

        else:
            self.add_widget(Image(source=score_text, allow_stretch=True,
                                  size_hint=(.4, .125), pos_hint={'x': .3, 'y': .6}))

            self.add_widget(Label(text=str(user.current_score), font_name='minecraft', font_size=128,
                                  outline_color=(255, 255, 255, 255), outline_width=4, color=(64, 75, 77, 1),
                                  size_hint=(.3, .15), pos_hint={'x': .35, 'y': .42}))

            self.add_widget(Image(source=highscore_text, allow_stretch=True,
                                  size_hint=(.4, .125), pos_hint={'x': .3, 'y': .3}))

            self.add_widget(Label(text=str(user.highscore), font_name='minecraft', font_size=128,
                                  outline_color=(255, 255, 255, 255), outline_width=4, color=(64, 75, 77, 1),
                                  size_hint=(.3, .15), pos_hint={'x': .35, 'y': .12}))
