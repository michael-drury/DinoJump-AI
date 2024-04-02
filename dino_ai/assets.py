import random
import pygame
import os

DEFAULT_JUMP_SPEED = 15
DEFAULT_GAME_SPEED = 15
DEFAULT_FPS = 60
DEFAULT_FRAMES_PER_IMAGE = 6


def load_images(name, num):
    return [
        pygame.image.load(os.path.join("images", name + "_" + str(x) + ".png"))
        for x in range(num)
    ]


class Dino:
    """
    A class representing a dinosaur character in a game, capable of running, jumping, and ducking.

    Note that the coordinate system used starts from the top left of the window

    Attributes:
        imgs_jump (list): Images used for the jumping animation.
        imgs_run (list): Images used for the running animation.
        imgs_run_duck (list): Images used for the ducking animation.
        imgs_cur (list): Currently active images based on the dino's state.
        img_index (int): Current index of the image to display from imgs_cur.
        frames_since_last_img_update (int): Counter for the frames elapsed since the last image change.
        fps (int): Frames per second, dictating the game's update rate.
        animation_rate (int): Number of frames to wait before switching to the next animation image.
        floor_pos_y (int): The y-coordinate of the floor position.
        x (int): The current x-coordinate of the dino.
        y (int): The current y-coordinate of the dino.
        duck_triggered (bool): Flag indicating whether the duck action has been triggered.
        jump_triggered (bool): Flag indicating whether the jump action has been triggered.
        frames_since_jump_start (int): Counter for the frames elapsed since the jump was initiated.
        gravity_normal (int): The gravity effect applied when not ducking [m/s^2].
        gravity_ducking (int): The gravity effect applied when ducking [m/s^2].
        jump_velocity (int): The initial velocity of the jump [m/s]

    Args:
        start_pos_x (int): The starting x-coordinate of the dino.
        floor_pos_y (int): The y-coordinate of the floor position.
        fps (int, optional): Frames per second for the game's update rate. Defaults to 60.
        frames_per_img_animate (int, optional): Number of frames to wait before switching to the next animation image. Defaults to DEFAULT_FRAMES_PER_IMAGE.
        gravity_normal (int, optional): The gravity effect applied when not ducking. Defaults to -10.
        gravity_ducking (int, optional): The gravity effect applied when ducking. Defaults to -15.
        jump_initial_velocity (int, optional): The initial velocity of the jump. Defaults to 15.
    """

    def __init__(
        self,
        start_pos_x,
        floor_pos_y,
        fps=DEFAULT_FPS,
        frames_per_img_animate=DEFAULT_FRAMES_PER_IMAGE,
        gravity_normal=-10,
        gravity_ducking=-15,
        jump_initial_velocity=DEFAULT_JUMP_SPEED,
    ):
        self.imgs_jump = load_images("dino_jump", 1)
        self.imgs_run = load_images("dino_run", 2)
        self.imgs_run_duck = load_images("dino_duck", 2)
        self.imgs_cur = self.imgs_run
        self.img_index = 0
        self.frames_since_last_img_update = 0
        self.fps = fps
        self.animation_rate = frames_per_img_animate
        self.floor_pos_y = floor_pos_y
        self.x = start_pos_x
        self.y = self._get_cur_img_floor_y()
        self.duck_triggered = False
        self.jump_triggered = False
        self.frames_since_jump_start = 0
        self.gravity_normal = gravity_normal
        self.gravity_ducking = gravity_ducking
        self.jump_velocity = jump_initial_velocity

    def _get_cur_img_floor_y(self):
        return self.floor_pos_y - self.imgs_cur[self.img_index].get_height()

    def _is_jumping(self):
        return self.frames_since_jump_start > 0

    def _animate_run(self):
        self.frames_since_last_img_update += 1
        if self.frames_since_last_img_update == self.animation_rate:
            self.img_index = not self.img_index
            self.frames_since_last_img_update = 0

    def _update_jump_elevation(self, gravity):

        time_since_last_frame = self.frames_since_jump_start / self.fps

        # NOTE: Use newtonian motion equation to determine dino height (s = ut + 0.5 * a * t^2)
        jump_elevation = (
            self.jump_velocity * time_since_last_frame
            + 0.5 * gravity * time_since_last_frame**2
        )

        if jump_elevation <= 0:
            self.y = self._get_cur_img_floor_y()
            self.frames_since_jump_start = 0
            return

        self.y = self._get_cur_img_floor_y() - jump_elevation

    def _update_cur_image(self):
        if self.jump_triggered or self._is_jumping():
            self.imgs_cur = self.imgs_jump

    def jump(self):
        self.jump_triggered = True

    def duck(self):
        self.duck_triggered = True

    def update(self):
        if self.jump_triggered or self._is_jumping():
            if self.duck_triggered:
                self.imgs_cur = self.imgs_run_duck
                gravity = self.gravity_ducking
            else:
                self.imgs_cur = self.imgs_jump
                self.img_index = 0
                gravity = self.gravity_normal
            self.frames_since_jump_start += 1
            self._update_jump_elevation(gravity)
        else:
            self.imgs_cur = self.imgs_run_duck if self.duck_triggered else self.imgs_run
            self.y = self.floor_pos_y - self.imgs_cur[self.img_index].get_height()
            self._animate_run()

        self.jump_triggered = False
        self.duck_triggered = False

    def get_image(self):
        return self.imgs_cur[self.img_index]

    def get_image_pos_x(self):
        return self.x

    def get_image_pos_y(self):
        return self.y

    def get_elevation(self):
        return self._get_cur_img_floor_y() - self.y


# TODO: Game speed param used here but frame rate used elsewhere
# TODO: Should population of these game elements be handled in this class or the game class?
# TODO: Maybe it doesn't make sense for all of these classes to hold fps if the reponsibility for this is at the game level?


# TODO: Make clear what coordinate system is being used in this instance
# ALWAYS USE TOP LEFT COORDINATE SYSTEM FOR SIMPLICITY
class _SceneElement:
    def __init__(self, fps, start_x, game_speed):
        if not isinstance(fps, int):
            raise TypeError("Expected fps to be an int")

        if not isinstance(start_x, int):
            raise TypeError("Expected start_x to be an int")

        if not isinstance(game_speed, int):
            raise TypeError("Expected game_speed to be an int")

        self.x = start_x
        self.y = None
        self.img = None
        self.fps = fps
        self.game_speed = game_speed

    def set_game_speed(self, speed):
        self.game_speed = speed

    def _update(self):
        self.x -= round((1 / self.fps) * self.game_speed)

    def get_image(self):
        return self.img

    def get_image_pos_x(self):
        return self.x

    def get_image_pos_y(self):
        return self.y


class Cactus(_SceneElement):
    def __init__(
        self,
        start_x,
        floor_y_pos,
        fps=DEFAULT_FRAMES_PER_IMAGE,
        game_speed=DEFAULT_GAME_SPEED,
        cactus_size=0,
    ):
        super().__init__(fps, start_x, game_speed)
        
        if cactus_size >= 3:
            raise ValueError("Cactus size should be either 0, 1 or 2")
        
        self.img = load_images("cactus", 3)[cactus_size]
        self.y = floor_y_pos - self.img.get_height()

    def update(self):
        self._update()


# NOTE: Y coordinate is at the top left
class Bird(_SceneElement):
    def __init__(
        self,
        start_x,
        min_y,
        max_y,
        game_speed=DEFAULT_GAME_SPEED,
        fps=DEFAULT_FPS,
        frames_per_img_animate=DEFAULT_FRAMES_PER_IMAGE,
    ):

        if not isinstance(frames_per_img_animate, int):
            raise TypeError("Expected frames_per_img_animate to be an int")

        if min_y >= max_y:
            raise ValueError("min_y is greater or equal to max_y")

        super().__init__(fps, start_x, game_speed)
        self.img_set = load_images("bird", 2)
        self.img_index = 0
        self.img = self.img_set[self.img_index]

        num_increments = 3
        bird_height_increment = (max_y - min_y) / (num_increments - 1)
        self.y = round(
            min_y + (bird_height_increment * random.randint(0, num_increments - 1))
        )
        self.frames_since_img_update = 0
        self.frames_per_img_animate = frames_per_img_animate

    def _animate(self):
        self.frames_since_img_update += 1
        if self.frames_since_img_update >= self.frames_per_img_animate:
            self.img_index = not self.img_index
            self.img = self.img_set[self.img_index]

    def update(self):
        self._animate()
        self._update()


class Dirt(_SceneElement):
    def __init__(
        self,
        start_x,
        min_y,
        max_y,
        min_rad=1,
        max_rad=4,
        game_speed=DEFAULT_GAME_SPEED,
        fps=DEFAULT_FPS,
    ):
        if min_y >= max_y:
            raise ValueError("min_y is greater or equal to max_y")

        super().__init__(fps, start_x, game_speed)

        num_increments = 30
        self.y = min_y + round(
            (max_y - min_y)
            / (num_increments - 1)
            * random.randint(0, num_increments - 1)
        )
        self.radius = random.randint(min_rad, max_rad)

    def get_radius(self):
        return self.radius

    def update(self):
        self._update()

    def get_image(self):
        raise NotImplementedError(
            "Dirt holds no image, this must be separatly generated"
        )
