from functools import partial
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from user_class import user

# // files used
main_theme = './Resources/audio/main_theme.mp3'
evil_laugh = './Resources/audio/zeus_evil_laugh.mp3'
thunder_sfx = './Resources/audio/thunder.mp3'


class MusicClient:
    """Class used to play music/sound effects"""

    def __init__(self):
        self.main_theme = SoundLoader.load(filename=main_theme)
        self.main_theme.loop = True

        self.evil_laugh = SoundLoader.load(filename=evil_laugh)
        self.evil_laugh.loop = False
        self.evil_laugh.volume = .5

        self.thunder_sfx = SoundLoader.load(filename=thunder_sfx)
        self.thunder_sfx.loop = False
        self.thunder_sfx.volume = .7

        self.event = None

    def play_main_theme(self) -> None:
        """Starts playing main theme"""

        if user.user_settings['music_on'] is True:
            self.main_theme.volume = .5
            self.main_theme.play()

    def stop_main_theme(self, play_laugh: bool) -> None:
        """Stops playing main theme"""

        self.event = Clock.schedule_interval(partial(self.lower_main_theme_volume, play_laugh), .05)

    def lower_main_theme_volume(self, play_laugh: bool, dt) -> None:
        """Lowers the main theme volume by a little bit so the music fades out"""

        try:
            self.main_theme.volume -= 0.02
        except OverflowError:
            self.main_theme.volume = 0

        if self.main_theme.volume <= 0:
            self.event.cancel()

            if play_laugh:
                self.play_evil_laugh()

    def play_evil_laugh(self) -> None:
        """Play demonic laugh"""

        if user.user_settings['sfx_on'] is True:
            self.evil_laugh.play()

    def play_thunder_sfx(self) -> None:
        """Play thunder impact sound effect"""

        if user.user_settings['sfx_on'] is True:
            self.thunder_sfx.play()


music_client = MusicClient()
