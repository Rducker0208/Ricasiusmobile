from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.switch import Switch

from database_class import db
from music_client import music_client
from user_class import user

# // images used
# // text acquired from: https://textcraft.net/
arrow_left = './Resources/settings_screen/arrow_to_left.png'
background_image = './Resources/settings_screen/temple_bg.png'
settings_text = './Resources/settings_screen/settings.png'
music_text = './Resources/settings_screen/Music.png'
sound_effects_text = './Resources/settings_screen/Sound-effects.png'
vibrations_text = './Resources/settings_screen/vibrations.png'

# // font
# // font acquired from: https://www.dafont.com/minecrafter.font
minecrafter_font = './Resources/fonts/Minecrafter.Reg.ttf'
LabelBase.register(name='minecraft', fn_regular=minecrafter_font)


class SetingsScreen(Screen):
    """Class that is used to display and update the user's settings"""

    def __init__(self, **kwargs):
        super(SetingsScreen, self).__init__(**kwargs)

        # // button that goes back to log in screen
        last_page_button = Button(background_normal=arrow_left, background_down=arrow_left,
                                  size_hint=(.3, .4), pos_hint={'x': -.08, 'y': .65})
        last_page_button.bind(on_press=self.go_to_start)

        # // Switch that controls wether or not to play music
        if user.user_settings['music_on'] is True:
            music_switch = Switch(active=True, size_hint=(.05, .05), pos_hint={'x': .47, 'y': .6})
        else:
            music_switch = Switch(active=False, size_hint=(.05, .05), pos_hint={'x': .47, 'y': .6})
        music_switch.bind(active=switch_music_setting)

        # // Switch that controls wether or not to play sound effects
        if user.user_settings['sfx_on'] is True:
            sfx_switch = Switch(active=True, size_hint=(.05, .05), pos_hint={'x': .47, 'y': .4})
        else:
            sfx_switch = Switch(active=False, size_hint=(.05, .05), pos_hint={'x': .47, 'y': .4})
        sfx_switch.bind(active=switch_sfx_setting)

        # // Switch that controls wether or not the device vibrates if available
        if user.user_settings['vibrations_on'] is True:
            vibrations_switch = Switch(active=True, size_hint=(.05, .05), pos_hint={'x': .47, 'y': .2})
        else:
            vibrations_switch = Switch(active=False, size_hint=(.05, .05), pos_hint={'x': .47, 'y': .2})
        vibrations_switch.bind(active=switch_vibration_setting)

        # // Button that opens the login menu
        switch_account_button = Button(font_name='minecraft', font_size=24, color=(0, 0, 0, 1),
                                       text='switch account',
                                       size_hint=(.2, .1), pos_hint={'x': .4, 'y': .05})
        switch_account_button.bind(on_press=self.switch_account)

        self.add_widget(SettingWidgets(last_page_button, music_switch, sfx_switch, vibrations_switch,
                                       switch_account_button))

    def go_to_start(self, instance) -> None: # noqa
        """Go back to the start menu"""

        self.manager.current = 'start'
        self.manager.remove_widget(self.manager.get_screen(name='settings'))

    def switch_account(self, instance) -> None: # noqa
        """Opens the login screen so the player can log in under a different name"""

        self.manager.current = 'login'
        self.manager.remove_widget(self.manager.get_screen(name='start'))
        self.manager.remove_widget(self.manager.get_screen(name='settings'))


class SettingWidgets(FloatLayout):
    """Class that comtains all the widgets for the settings screen"""

    def __init__(self, last_page_button, music_switch, sfx_switch, vibrations_switch, switch_account_button,
                 **kwargs):
        super(SettingWidgets, self).__init__(**kwargs)

        self.last_page_button = last_page_button
        self.music_switch = music_switch
        self.sfx_switch = sfx_switch
        self.vibrations_switch = vibrations_switch
        self.switch_account_button = switch_account_button

        self.add_widget(Image(source=background_image, allow_stretch=True, keep_ratio=False))

        self.add_widget(Image(source=settings_text, allow_stretch=True,
                              size_hint=(.4, .15), pos_hint={'x': .3, 'y': .8}))

        self.add_widget(last_page_button)

        self.add_widget(Image(source=music_text, allow_stretch=True,
                              size_hint=(.25, .1), pos_hint={'x': .375, 'y': .68}))
        self.add_widget(self.music_switch)

        self.add_widget(Image(source=sound_effects_text, allow_stretch=True,
                              size_hint=(.25, .1), pos_hint={'x': .375, 'y': .48}))
        self.add_widget(self.sfx_switch)

        self.add_widget(Image(source=vibrations_text, allow_stretch=True,
                              size_hint=(.25, .1), pos_hint={'x': .375, 'y': .28}))
        self.add_widget(self.vibrations_switch)

        self.add_widget(switch_account_button)


def switch_music_setting(instance, switch_state) -> None: # noqa
    """Turns off/on music depending on the user's old setting"""

    if user.user_settings['music_on'] is True:
        user.user_settings['music_on'] = False
        music_client.stop_main_theme(False)
    else:
        user.user_settings['music_on'] = True
        music_client.play_main_theme()

    db.update_user_settings(user.username, str(user.user_settings))


def switch_sfx_setting(instance, switch_state) -> None:  # noqa
    """Turns off/on sound effects depending on the user's old setting"""

    if user.user_settings['sfx_on'] is True:
        user.user_settings['sfx_on'] = False
    else:
        user.user_settings['sfx_on'] = True

    db.update_user_settings(user.username, str(user.user_settings))


def switch_vibration_setting(instance, switch_state) -> None:  # noqa
    """Turns off/on vibrations depending on the user's old setting"""

    if user.user_settings['vibrations_on'] is True:
        user.user_settings['vibrations_on'] = False
    else:
        user.user_settings['vibrations_on'] = True

    db.update_user_settings(user.username, str(user.user_settings))
