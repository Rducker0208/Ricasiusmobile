from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from database_class import db
from start_screen import StartScreen
from user_class import user

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
                                     size_hint=(.4, .05), pos_hint={'x': .3, 'y': .48})
        username_textbox.bind(on_text_validate=self.check_username)

        self.add_widget(login_screen_widgets(username_textbox))

    def check_username(self, instance) -> None:
        """Check if the player passed a non-empty string"""

        if instance.text:
            with open('username.txt', 'w') as f:
                f.write(instance.text)
                user.username = instance.text
                user.highscore = db.load_user(user.username)
                user.create_score_image(mode='highscore')
                print(f'loaded highscore for {user.username}: {user.highscore}')

                # // Readd start screen so highscore can be refreshed
                self.manager.add_widget(StartScreen(name='start'))
                self.manager.current = 'start'


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





