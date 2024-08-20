from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen


# // image directory
player_images_dir = './Resources/game_screen/player'


class Player:
    """Class that handles actions from player such as walking and placing the player on screen"""

    def __init__(self):
        self.player = Image(source=f'{player_images_dir}/player_idle_right_1.png',
                            size_hint=(.1, .15), allow_stretch=True,
                            x=Window.size[0] // 2 - Window.size[0] // 20,
                            y=Window.size[1] // 2 - Window.size[1] // 10)

        self.hp = 5

        # // variables used for graphical purposes
        self.x_axis = 'left'
        self.y_axis = 'up'

        self.base_speed = Window.size[0] // 75
        self.speed_x = 0
        self.speed_y = 0

        self.frames_since_sprite_change = 0

    def update_player(self, screen: Screen) -> None:
        """Update player sprite status and location based on joystick input"""

        screen.remove_widget(self.player)

        # // See if player is idle or walking
        if self.speed_x == 0 and self.speed_y == 0:

            # // animation updates every 2 frames
            if self.frames_since_sprite_change == 1:
                self.frames_since_sprite_change = 0

                # // Check if player animation is at its end, restart if needed
                # self.player.source = f'{player_images_dir}/player_idle_1.png'
                if self.player.source[-5] == '8':
                    self.player.source = f'{player_images_dir}/player_idle_{self.x_axis}_1.png'
                else:
                    self.player.source = f'{player_images_dir}/player_idle_{self.x_axis}_{int(self.player.source[-5]) + 1}.png'

            else:
                self.frames_since_sprite_change += 1

        else:
            # // player is not idle
            if self.frames_since_sprite_change == 1:
                self.frames_since_sprite_change = 0

                # // Set correct image
                if self.player.source[-5] == '8':
                    self.player.source = f'{player_images_dir}/player_walk_{self.x_axis}_1.png'
                else:
                    self.player.source = \
                        f'{player_images_dir}/player_walk_{self.x_axis}_{int(self.player.source[-5]) + 1}.png'
            else:
                self.frames_since_sprite_change += 1

            # // check if player is within boundaries
            if self.x_axis == 'right':
                if self.player.x < Window.size[0] - self.player.size[0] - 20:
                    self.player.x += self.base_speed * self.speed_x
            else:

                # // Check if player is not to close to the joystick
                if self.player.y <= Window.size[1] / 2.8:
                    if self.player.x > Window.size[0] / 4:
                        self.player.x -= self.base_speed * (self.speed_x * -1)

                # // Gets triggered if player is above the joystick on screen
                elif self.player.x > 0:
                    self.player.x -= self.base_speed * (self.speed_x * -1)

            if self.y_axis == 'up':
                if self.player.y < Window.size[1] - Window.size[1] / 2.5:
                    self.player.y += self.base_speed * self.speed_y
            else:
                # // Check if player is not to close to the joystick
                if self.player.x <= Window.size[0] / 4:
                    if self.player.y > Window.size[1] / 2.2:
                        self.player.y -= self.base_speed * (self.speed_y * -1)
                else:
                    if self.player.y > 5:
                        self.player.y -= self.base_speed * (self.speed_y * -1)




                # # // Gets triggered if player is to the right of the joystick on screen
                # elif self.player.y <= Window.size[1] / 5 + Window.size[1] // 15:
                #     self.player.y -= self.base_speed * (self.speed_y * -1)

                # if self.player.y  Window.size[1] / 2.8:
                # if self.player.y > 20:
                #     self.player.y -= self.base_speed * (self.speed_y * -1)

        screen.add_widget(self.player)

player = Player()