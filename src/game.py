import src.assets as assets
import src.render as render
import src.mechanics as mechanics

import random
import pygame

from collections import namedtuple

TITLE = "Dino Jump"

Obstacle = namedtuple(
    "Obstacle", ["height", "width", "distance", "elevation", "is_cactus"]
)

NUM_DIRT_PIECES = 20
DIRT_SPREAD = 30

DINO_JUMP_VELOCITY = 50
DINO_SPEED_INCREMENT = 0.005


class Game:
    """
    A class for managing gameplay in Dino Jump. It integrates all game components, including dinosaurs, obstacles, and environmental elements.
    
    Handles game initialisation, game state management, updates game elements, and renders the game scene.
    """
    def __init__(self, numDinos, win_width, win_height, frame_rate=30, start_speed=15):

        if numDinos == 0:
            raise ValueError("Can't init game without dinos")

        floor_height = round((win_height * 7) / 8)
        self.render = render.Render(
            TITLE,
            win_width,
            win_height,
            floor_height,
        )
        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()
        self.dino_speed = start_speed
        self.floor_dirt: list[assets.Dirt] = []
        self._generate_dirt()

        start_pos_x = win_width / 10
        self.dinos: list[assets.Dino] = [
            assets.Dino(
                start_pos_x,
                floor_height,
                frame_rate,
                jump_initial_velocity=DINO_JUMP_VELOCITY,
            )
            for _ in range(numDinos)
        ]
        self.score = 0
        self.obstacles = []
        self._populate_screen_with_obstacles()

    def _generate_dirt(self):
        for i in range(NUM_DIRT_PIECES):
            dirt_x = i * (self.render.win_width / NUM_DIRT_PIECES)
            self.floor_dirt.append(
                assets.Dirt(
                    int(dirt_x),
                    self.render.floor_height,
                    self.render.floor_height + DIRT_SPREAD,
                    game_speed=self.dino_speed,
                    fps=self.frame_rate,
                )
            )

    def _obstacle_off_screen(self, obstacle):
        return obstacle.x < -obstacle.img.get_width()

    def _delete_obstacles_not_visible(self):
        for obst in self.obstacles:
            if self._obstacle_off_screen(obst):
                self.obstacles.remove(obst)

    def _populate_screen_with_obstacles(self):
        while len(self.obstacles) != 3:

            if self.obstacles:
                x_pos = self.obstacles[-1].x + random.randint(
                    int(self.render.win_width / 3), int(self.render.win_width / 2)
                )
            else:
                x_pos = self.render.win_width + 50

            rand_num = random.randint(0, 3)
            if rand_num == 3:
                self.obstacles.append(
                    assets.Bird(
                        x_pos,
                        self.render.win_height / 5,
                        self.render.floor_height,
                        game_speed=self.dino_speed,
                        fps=self.frame_rate,
                    )
                )
            else:
                self.obstacles.append(
                    assets.Cactus(
                        x_pos,
                        self.render.floor_height,
                        cactus_size=rand_num,
                        game_speed=self.dino_speed,
                        fps=self.frame_rate,
                    )
                )

    def _update_dirt(self):
        for dirt in self.floor_dirt:
            dirt.set_game_speed(self.dino_speed)
            dirt.update()
            if dirt.get_image_pos_x() < 0:
                dirt.set_x(self.render.win_width + 10)

    def _update_obstacles(self):
        for obst in self.obstacles:
            obst.set_game_speed(self.dino_speed)
            obst.update()

    def _obstacle_in_front_of_dino(self, obstacle, dino):
        return obstacle.x + obstacle.img.get_width() > dino.x

    def _get_next_obstacle(self, dinoId):
        obstacle_index = 0
        while not self._obstacle_in_front_of_dino(
            self.obstacles[obstacle_index], self.dinos[dinoId]
        ):
            obstacle_index += 1

        return self.obstacles[obstacle_index]

    def restrict_game_loop_speed(self):
        self.clock.tick(self.frame_rate)

    def increment_game_speed(self):
        self.dino_speed += DINO_SPEED_INCREMENT

    def window_closed(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def quit_game(self):
        self.render.close_window()

    def get_dino_elevation(self, dinoIndex):
        return self.dinos[dinoIndex].get_elevation()

    def get_game_speed(self):
        return self.dino_speed

    def increment_score(self):
        self.score += 1

    def get_next_obstacle_info(self, dinoId):

        next_obstacle = self._get_next_obstacle(dinoId)

        distance = next_obstacle.x - (
            self.dinos[dinoId].x + self.dinos[dinoId].get_image().get_width()
        )
        height = next_obstacle.img.get_height()
        width = next_obstacle.img.get_width()
        elevation = self.render.floor_height - (
            next_obstacle.y + next_obstacle.img.get_height()
        )
        is_cactus = isinstance(next_obstacle, assets.Cactus)

        return Obstacle(height, width, distance, elevation, is_cactus)

    def update_environment(self):
        self._delete_obstacles_not_visible()
        self._populate_screen_with_obstacles()
        self._update_dirt()
        self._update_obstacles()

    def dino_jump(self, dinoIndex):
        self.dinos[dinoIndex].jump()

    def dino_duck(self, dinoIndex):
        self.dinos[dinoIndex].duck()

    def update_dino(self, dinoIndex):
        self.dinos[dinoIndex].update()

    def dino_object_collision(self, dinoIndex):
        for obstacle in self.obstacles:

            dino = self.dinos[dinoIndex]

            if mechanics.collision(
                obstacle.get_image(),
                obstacle.get_image_pos_x(),
                obstacle.get_image_pos_y(),
                dino.get_image(),
                dino.get_image_pos_x(),
                dino.get_image_pos_y(),
            ):
                dino.set_dead()
                return True
        return False

    def draw_game(self):
        self.render.set_background_white()
        self.render.display_floor()
        self.render.display_score(self.score)
        for dino in self.dinos:
            if dino.is_dead():
                continue
            self.render.draw_img(
                dino.get_image(), dino.get_image_pos_x(), dino.get_image_pos_y()
            )
        for dirt in self.floor_dirt:
            self.render.draw_circle(
                dirt.get_radius(), dirt.get_image_pos_x(), dirt.get_image_pos_y()
            )
        for obst in self.obstacles:
            self.render.draw_img(
                obst.get_image(), obst.get_image_pos_x(), obst.get_image_pos_y()
            )

    def get_renderer(self):
        return self.render
