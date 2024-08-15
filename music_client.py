from kivy.core.audio import SoundLoader

# // files used
main_theme = './Resources/audio/main_theme.mp3'
evil_laugh = './Resources/audio/zeus_evil_laugh.mp3'
thunder_sfx = './Resources/audio/thunder.mp3'


class MusicClient:
    """Class used to play music/sound effects"""

    def __init__(self):
        self.main_theme = SoundLoader.load(filename=main_theme)
        self.main_theme.loop = True
        self.main_theme.volume = .5

        self.evil_laugh = SoundLoader.load(filename=evil_laugh)
        self.evil_laugh.loop = False
        self.evil_laugh.volume = .5

        self.thunder_sfx = SoundLoader.load(filename=thunder_sfx)
        self.thunder_sfx.loop = False
        self.thunder_sfx.volume = .7

    def play_main_theme(self) -> None:
        """Starts playing main theme"""

        self.main_theme.play()

    def stop_main_theme(self) -> None:
        """Stops playing main theme"""

        self.main_theme.stop()

    def play_evil_laugh(self) -> None:
        """Play demonic laugh"""

        self.evil_laugh.play()

    def play_thunder_sfx(self) -> None:
        """Play thunder impact sound effect"""

        self.thunder_sfx.play()


music_client = MusicClient()
