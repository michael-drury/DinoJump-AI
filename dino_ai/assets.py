import random
import dino_ai.settings as settings
import dino_ai.render as render
import pygame
import os


def load_images(name, num):
    return [
        pygame.image.load(os.path.join("images", name + "_" + str(x) + ".png"))
        for x in range(num)
    ]


# TODO: Feed in settings on init to remove settings accross all files
class Dino:
    def __init__(self):
        self.img_jump = load_images("dino_jump", 1)
        self.imgs_run = load_images("dino_run", 2)
        self.imgs_run_duck = load_images("dino_duck", 2)
        self.imgs_cur = self.imgs_run
        self.img_index = 0
        self.img_frames = 0
        self.x = settings.DINO_START_POSITION_X
        self.y = self._get_cur_img_floor_y()
        self.duck_triggered = False
        self.jump_triggered = False
        self.jump_frames = 0

    def _get_cur_img_floor_y(self):
        return settings.ENV_FLOOR_HEIGHT - self.imgs_cur[self.img_index].get_height()

    def _is_touching_floor(self):
        return self.y >= self._get_cur_img_floor_y()

    def _is_jumping(self):
        return self.jump_frames > 0

    def _animate_run(self):
        self.img_frames += 1
        if self.img_frames != settings.FRAMES_PER_IMAGE_ANIMATE:
            self.img_index = not self.img_index
            self.img_frames = 0

    def _update_jump_elevation(self, gravity):
        self.jump_frames += 1
        time_since_last_frame = self.jump_frames / settings.FRAME_RATE
        # Use newtonian motion equation to determine dino height (s = ut + 0.5 * a * t^2)
        self.y += (
            -settings.DINO_JUMP_VELOCITY * time_since_last_frame
            + 0.5 * -gravity * time_since_last_frame**2
        )

        if self._is_touching_floor():
            self.y = self._get_cur_img_floor_y()
            self.jump_frames = 0

    def _update_cur_image(self):
        if self.jump_triggered or self._is_jumping():
            self.imgs_cur = self.img_jump

    def jump(self):
        self.jump_triggered = True

    def duck(self):
        self.duck_triggered = True

    def update(self):
        
        # TODO: If we update img, also need to update self.y?? As this top left of picture
        # TODO: Could de-couple self.y?
        # TODO: How was this handled in the previous verison?
        #  - Set self.y to floor - image_height when running
        if self.jump_triggered or self._is_jumping():
            if self.duck_triggered:
                self.imgs_cur = self.imgs_run_duck
                gravity = settings.DINO_GRAVITY_DUCKING
            else:
                self.imgs_cur = self.img_jump
                self.img_index = 0
                gravity = settings.DINO_GRAVITY_NORMAL
            self._update_jump_elevation(gravity)
        else:
            self.imgs_cur = self.imgs_run_duck if self.duck_triggered else self.imgs_run
            self.y = settings.ENV_FLOOR_HEIGHT - self.imgs_cur[self.img_index].get_height()
            self._animate_run()

        self.jump_triggered = False
        self.duck_triggered = False

    def get_image(self):
        return self.imgs_cur[self.img_index]

    def get_img_pos_x(self):
        return self.x

    def get_img_pos_y(self):
        return self.y

    def get_elevation(self):
        return self._get_cur_img_floor_y() - self.y

class Obstacles:
    def __init__(self, x):
        self.x = x
        self.y = None
        self.img = None

    def move(self, gameSpeed):
        self.x -= gameSpeed

    def _draw(self):
        render.draw_img(self.img, self.x, self.y)


class Cactus(Obstacles):
    def __init__(self, x, size):
        super().__init__(x)
        # TODO: Test to check for correct size input
        self.img = load_images("cactus", 3)[size]
        # This uses a function that's available from other class
        self.y = settings.ENV_FLOOR_HEIGHT - self.img.get_height()

    def draw(self):
        self._draw()


class Bird(Obstacles):
    def __init__(self, x):
        super().__init__(x)
        self.imgs = load_images("bird", 2)
        self.img_cur = self.imgs[1]
        self.y = settings.ENV_FLOOR_HEIGHT - 90 * random.randint(1, 3)
        self.img_count = 0

    def draw(self):
        animate(self, self.imgs)
        self._draw()


class Dirt:
    def __init__(self, x):
        self.x = x
        self.y = settings.ENV_FLOOR_HEIGHT - 15 + random.randint(0, 30)
        self.radius = random.randint(0, 4)

    # Keep win at render level?
    def draw(self):
        pygame.draw.circle(
            WIN, render.BLACK, (round(self.x), round(self.y)), self.radius
        )

    def move(self, gameSpeed):
        self.x -= gameSpeed
        if self.x < -self.radius:
            self.x = settings.WIN_WIDTH + self.radius
