from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from database_class import db
from user_class import user
from .start_screen import StartScreen

# // images used
# // text acquired from: https://textcraft.net/
background_image = './Resources/login_screen/temple_bg.png'
login_text = './Resources/login_screen/Login.png'
enter_username_text = './Resources/login_screen/Enter-username.png'
required_once_text = './Resources/login_screen/required-once-per-update.png'


class LoginScreen(Screen):
    """Class that handles the screen in which player's on non-windows need to log in upon first login"""

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        username_textbox = TextInput(text='', multiline=False,
                                     size_hint=(.4, .1), pos_hint={'x': .295, 'y': .4})
        username_textbox.bind(on_text_validate=self.check_username)

        self.add_widget(login_screen_widgets(username_textbox))

    def check_username(self, instance) -> None:
        """Check if the player passed a non-empty string"""

        if instance.text:

            # // load user info from username
            with open('username.txt', 'w') as f:

                # // save new username to username file
                f.write(instance.text)

                # // save user info
                user.username = instance.text
                user_info = db.load_user_info(user.username)
                user.highscore = int(user_info[0])
                user.user_settings = eval(user_info[1])
                print(f'loaded highscore for {user.username}: {user.highscore}')

                # // Readd start screen so highscore can be refreshed
                self.manager.add_widget(StartScreen(name='start'))
                self.manager.current = 'start'

                self.manager.remove_widget(self.manager.get_screen(name='login'))


class login_screen_widgets(FloatLayout):
    """Class containing all widgets for login screen"""
    
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





