from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from database_class import db
from music_client import music_client
from user_class import user
from .start_screen import StartScreen

# // images used
# // text acquired from: https://textcraft.net/
background_image = './Resources/login_screen/temple_bg.png'
login_text = './Resources/login_screen/Login.png'
enter_username_text = './Resources/login_screen/Enter-username.png'
required_once_text = './Resources/login_screen/required-once-per-update.png'


class LoginScreen(Screen):
    """Screen containing a username textbox that users need to fill in when they log in for the first time or
     when they want to switch accounts"""

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        username_textbox = TextInput(text='', multiline=False,
                                     size_hint=(.4, .1), pos_hint={'x': .295, 'y': .4})
        username_textbox.bind(on_text_validate=self.check_username)

        self.add_widget(login_screen_widgets(username_textbox))

    def check_username(self, instance) -> None:
        """Check if the player passed a non-empty string"""

        if instance.text:

            username = instance.text.replace("'", '')
            username = username.replace('"', '')

            # // load user info from username
            with open('username.txt', 'w') as f:

                # // Save new username to username file
                f.write(username)

                # // Save user info
                user.username = username
                user_info = db.load_user_info(user.username)
                user.highscore = int(user_info[0])
                user.user_settings = eval(user_info[1])
                if user.user_has_speakers:
                    music_client.music_volume = user.user_settings['music_volume']
                    music_client.sfx_volume = user.user_settings['sfx_volume']

                # // Readd start screen so highscore can be refreshed
                self.manager.add_widget(StartScreen(name='start'))
                self.manager.current = 'start'
                if user.user_has_speakers:
                    music_client.play_main_theme()


class login_screen_widgets(FloatLayout):
    """This layout contains all the graphical aspects of the widgets that are actually shown on this screen"""
    
    def __init__(self, username_textbox, **kwargs):
        super(login_screen_widgets, self).__init__(**kwargs)

        self.add_widget(Image(source=background_image, allow_stretch=True, keep_ratio=False))

        self.add_widget(Image(source=login_text, allow_stretch=True,
                              size_hint=(.58, .25), pos_hint={'x': .2, 'y': .7}))

        self.add_widget(Image(source=enter_username_text, allow_stretch=True,
                              size_hint=(.5, .15), pos_hint={'x': .25, 'y': .5}))

        self.add_widget(username_textbox)

        self.add_widget(Image(source=required_once_text, allow_stretch=True,
                              size_hint=(.5, .15), pos_hint={'x': .24, 'y': .1}))





