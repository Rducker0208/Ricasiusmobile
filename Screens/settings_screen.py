from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.switch import Switch

# // images used
# // text acquired from: https://textcraft.net/
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

        music_switch = Switch(active=True, size_hint=(.2, .2), pos_hint={'x': .4, 'y': .53})
        sfx_switch = Switch(active=True, size_hint=(.2, .2), pos_hint={'x': .4, 'y': .33})
        vibrations_switch = Switch(active=True, size_hint=(.2, .2), pos_hint={'x': .4, 'y': .13})
        credits_button = Button(text='credits', font_name='minecraft', color=(0,0,0,1),
                                size_hint=(.2, .1), pos_hint={'x': .3, 'y': .05})
        switch_account_button = Button(text='switch account', font_name='minecraft', color=(0,0,0,1),
                                       size_hint=(.2, .1), pos_hint={'x': .5, 'y': .05})

        self.add_widget(SettingWidgets(music_switch, sfx_switch, vibrations_switch,
                                       credits_button, switch_account_button))

    def switch_music_setting(self) -> None:
        """Turns off/on music depending on the user's old setting"""

        ...

    def switch_sfx_setting(self) -> None:
        """Turns off/on sound effects depending on the user's old setting"""

        ...

    def switch_vibration_setting(self) -> None:
        """Turns off/on vibrations depending on the user's old setting"""

        ...

    def show_credits(self) -> None:
        """Opens the credits screen"""

        ...

    def switch_account(self) -> None:
        """Opens the login screen so the player can log in under a different name"""

        ...


class SettingWidgets(FloatLayout):
    """Class that comtains all the widgets for the settings screen"""

    def __init__(self, music_switch, sfx_switch, vibrations_switch, credits_button, switch_account_button,
                 **kwargs):
        super(SettingWidgets, self).__init__(**kwargs)

        self.music_switch = music_switch
        self.sfx_switch = sfx_switch
        self.vibrations_switch = vibrations_switch
        self.credits_button = credits_button
        self.switch_account_button = switch_account_button

        self.add_widget(Image(source=background_image, allow_stretch=True, keep_ratio=False))

        self.add_widget(Image(source=settings_text, allow_stretch=True,
                              size_hint=(.4, .15), pos_hint={'x': .3, 'y': .8}))

        self.add_widget(Image(source=music_text, allow_stretch=True,
                              size_hint=(.25, .1), pos_hint={'x': .375, 'y': .68}))
        self.add_widget(self.music_switch)

        self.add_widget(Image(source=sound_effects_text, allow_stretch=True,
                              size_hint=(.25, .1), pos_hint={'x': .375, 'y': .48}))
        self.add_widget(self.sfx_switch)

        self.add_widget(Image(source=vibrations_text, allow_stretch=True,
                              size_hint=(.25, .1), pos_hint={'x': .375, 'y': .28}))
        self.add_widget(self.vibrations_switch)

        self.add_widget(credits_button)
        self.add_widget(switch_account_button)


