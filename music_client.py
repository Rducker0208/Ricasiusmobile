from functools import partial
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from user_class import user

# // sound files used
evil_laugh = './Resources/audio/zeus_evil_laugh.mp3'
main_theme = './Resources/audio/main_theme.mp3'
shield_breaking_sfx = './Resources/audio/shield_breaking.mp3'
thunder_sfx = './Resources/audio/thunder.mp3'
vase_breaking_sfx = './Resources/audio/vase_breaking.mp3'


class MusicClient:
    """Class used to play music/sound effects"""

    def __init__(self):

        # // Check if the user is already logged in, if not set a value of 0 and these will get set later
        try:
            self.music_volume = user.user_settings['music_volume']
            self.sfx_volume = user.user_settings['sfx_volume']
        except TypeError:
            self.music_volume = 0.0
            self.sfx_volume = 0.0

        # // load all the files
        self.main_theme = SoundLoader.load(filename=main_theme)
        self.evil_laugh = SoundLoader.load(filename=evil_laugh)
        self.shield_breaking_sfx = SoundLoader.load(filename=shield_breaking_sfx)
        self.thunder_sfx = SoundLoader.load(filename=thunder_sfx)
        self.vase_breaking_sfx = SoundLoader.load(filename=vase_breaking_sfx)

        self.main_theme.loop = True

    def play_main_theme(self) -> None:
        """Starts playing main theme"""

        self.main_theme.volume = self.music_volume
        self.main_theme.play()

    def update_music_volume(self) -> None:
        """Update main theme volume"""

        self.main_theme.volume = self.music_volume

    def stop_main_theme(self, play_laugh: bool, dt: float) -> None:
        """Slowly fade out main theme"""

        # // Due to binary limitations sometimes the number becomes to big
        try:
            self.main_theme.volume -= 0.03
        except OverflowError:
            self.main_theme.volume = 0

        # // Check if the evil laugh should be played
        if self.main_theme.volume <= 0:
            if play_laugh:
                self.play_evil_laugh()
        else:
            # // Set a recursive clock event that keeps decreasing the music volume
            Clock.schedule_once(partial(self.stop_main_theme, play_laugh), .05)

    def play_evil_laugh(self) -> None:
        """Play demonic laugh"""

        self.evil_laugh.volume = self.sfx_volume
        self.evil_laugh.play()

    def play_thunder_sfx(self) -> None:
        """Play thunder impact sound effect"""

        self.thunder_sfx.volume = self.sfx_volume
        self.thunder_sfx.play()

    def play_vase_breaking_sfx(self) -> None:
        """Play sound effect of a vase breaking"""

        self.vase_breaking_sfx.volume = self.sfx_volume
        self.vase_breaking_sfx.play()

    def play_shield_breaking_sfx(self) -> None:
        """Play sound effect of a shield breaking"""

        self.shield_breaking_sfx.volume = self.sfx_volume
        self.shield_breaking_sfx.play()


music_client = MusicClient()
