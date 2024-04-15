import random
import pygame
import os

PIX_PER_METER = 15

DEFAULT_JUMP_SPEED_MPS = 40
DEFAULT_GAME_SPEED_MPS = 15
DEFAULT_FPS = 60
DEFAULT_FRAMES_PER_IMAGE = 5


def load_images(name, num):
    return [
        pygame.image.load(os.path.join("images", name + "_" + str(x) + ".png"))
        for x in range(num)
    ]


class Dino:
    """
    Dinosaur character, capable of running, jumping, and ducking.

    Note that the origin of the coordinate system used starts from the top left of the window.
    """

    def __init__(
        self,
        start_pos_x,
        floor_pos_y,
        fps=DEFAULT_FPS,
        frames_per_img_animate=DEFAULT_FRAMES_PER_IMAGE,
        gravity_normal=-50,
        gravity_ducking=-70,
        jump_initial_velocity=DEFAULT_JUMP_SPEED_MPS,
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
        self.dead = False

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
        jump_elevation_meters = (
            self.jump_velocity * time_since_last_frame
            + 0.5 * gravity * time_since_last_frame**2
        )

        jump_elevation_px = jump_elevation_meters * PIX_PER_METER

        if jump_elevation_px <= 0:
            self.y = self._get_cur_img_floor_y()
            self.frames_since_jump_start = 0
            return

        self.y = self._get_cur_img_floor_y() - jump_elevation_px

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

    def set_dead(self):
        self.dead = True

    def is_dead(self):
        return self.dead


class _SceneElement:
    """
    Abstract base class for common functionalities of elements that appear within the game scene.
    
    Provides basic attributes and methods needed for managing these elements, such as their position and movement across the game window.
    
    Note that the origin of the coordinate system used starts from the top left of the window.
    """

    def __init__(self, fps, start_x, game_speed):
        if not isinstance(fps, int):
            raise TypeError("Expected fps to be an int")

        if not isinstance(start_x, int):
            raise TypeError("Expected start_x to be an int")

        if not isinstance(game_speed, float) and not isinstance(game_speed, int):
            raise TypeError("Expected game_speed to be am int/ float")

        self.x = start_x
        self.y = None
        self.img = None
        self.fps = fps
        self.set_game_speed(game_speed)

    def set_game_speed(self, speed):
        self.game_speed = speed * PIX_PER_METER

    def _update(self):
        distance = round(self.game_speed / self.fps)
        self.x -= distance

    def get_image(self):
        return self.img

    def get_image_pos_x(self):
        return self.x

    def get_image_pos_y(self):
        return self.y


class Cactus(_SceneElement):
    """
    A subclass of _SceneElement that represents cactus obstacles in the game.

    Cactuses move horizontally across the screen and vary in size.

    Note that the origin of the coordinate system used starts from the top left of the window.
    """

    def __init__(
        self,
        start_x,
        floor_y_pos,
        fps=DEFAULT_FRAMES_PER_IMAGE,
        game_speed=DEFAULT_GAME_SPEED_MPS,
        cactus_size=0,
    ):
        super().__init__(fps, start_x, game_speed)

        if cactus_size >= 3:
            raise ValueError("Cactus size should be either 0, 1 or 2")

        self.img = load_images("cactus", 3)[cactus_size]
        self.y = floor_y_pos - self.img.get_height()

    def update(self):
        self._update()


class Bird(_SceneElement):
    """
    A subclass of _SceneElement representing flying birds as obstacles.

    Birds can appear at different heights and animate between two images to simulate flying.
    
    Note that the origin of the coordinate system used starts from the top left of the window.
    """

    def __init__(
        self,
        start_x,
        min_y,
        max_y,
        game_speed=DEFAULT_GAME_SPEED_MPS,
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

        max_y = max_y - self.img.get_height()
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

            self.frames_since_img_update = 0

    def update(self):
        self._animate()
        self._update()


class Dirt(_SceneElement):
    """
    A subclass of _SceneElement that represents random dirt particles on the game screen.
    
    Note that the origin of the coordinate system used starts from the top left of the window.
    """

    def __init__(
        self,
        start_x,
        min_y,
        max_y,
        min_rad=1,
        max_rad=4,
        game_speed=DEFAULT_GAME_SPEED_MPS,
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

    def set_x(self, x):
        self.x = x

    def get_radius(self):
        return self.radius

    def update(self):
        self._update()

    def get_image(self):
        raise NotImplementedError(
            "Dirt holds no image, this must be separatly generated"
        )
