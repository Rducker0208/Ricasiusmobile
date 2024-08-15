from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.switch import Switch


class SetingsScreen(Screen):
    """Class that is used to display and update the user's settings"""

    def __init__(self, **kwargs):
        super(SetingsScreen, self).__init__(**kwargs)

        self.add_widget(Switch(active=True))


class SettingWidgets(FloatLayout):
    """Class that comtains all the widgets for the settings screen"""

    def __init__(self, music_switch, sfx_switch, **kwargs):
        super(SettingWidgets, self).__init__(**kwargs)

        self.music_switch = music_switch
        self.sfx_switch = sfx_switch



