import dino_ai.settings as settings
import dino_ai.assets as assets
import random
import render
import mechanics
import pygame

from collections import namedtuple

Obstacle = namedtuple(
    "Obstacle", ["height", "width", "distance", "elevation", "is_cactus"]
)

# Can mock pygame as render is handling it!

# TODO: Oranise methods. Set _ for private methods
# TODO: Abstract out pygame from Game so same level of access


class Game:
    def __init__(self, numDinos):
        
        if numDinos == 0:
            raise ValueError("Can't init game without dinos")
        
        self.render = render.Render(
            settings.GAME_TITLE,
            settings.WIN_WIDTH,
            settings.WIN_HEIGHT,
            settings.ENV_FLOOR_HEIGHT,
        )
        self.clock = pygame.time.Clock()
        self.dino_speed = settings.DINO_INITIAL_SPEED
        self.floor_dirt = []
        self._generate_dirt()
        self.dinos = [assets.Dino() in range(numDinos)]
        self.score = 0
        self.obstacles = []
        self.populate_screen_with_obstacles()
        
    def _generate_dirt(self):
        for i in range(settings.ENV_NUM_DIRT_PIECES):
            dirt_x = i * (settings.WIN_WIDTH / settings.ENV_NUM_DIRT_PIECES)
            self.floor_dirt.append(assets.Dirt(int(dirt_x)))
    
    def restrict_game_loop_speed(self):
        self.clock.tick(settings.FRAME_RATE)

    def increment_dino_speed(self):
        self.dino_speed += settings.DINO_SPEED_INCREMENT / settings.FRAME_RATE

    def window_closed(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def quit_game(self):
        self.render.close_window()

    def get_dino_elevation(self, dinoIndex):
        return self.dinos[dinoIndex].get_elevation()

    def get_dino_speed(self):
        return self.dino_speed

    def increment_score(self):
        self.score += 1

    # TODO: How should this be handled if self not required?
    # Tale index argument instead?
    def obstacle_off_screen(obstacle):
        return obstacle.x < -obstacle.img.get_width()

    def delete_obstacles_not_visible(self, obstacles):
        for obst in obstacles:
            if self.obstacle_off_screen(obst):
                obstacles.remove(obst)

    def populate_screen_with_obstacles(self):
        while len(self.obstacles) != 3:

            if self.obstacles:
                x_pos = self.obstacles[-1].x + random.randint(400, 600)
            else:
                x_pos = settings.WIN_WIDTH + 50

            rand_num = random.randint(0, 3)
            if rand_num == 3:
                self.obstacles.append(assets.Bird(x_pos))
            else:
                self.obstacles.append(assets.Cactus(x_pos, rand_num))

    def obstacle_in_front_of_dino(obstacle, dino):
        return obstacle.x + obstacle.img.get_width > dino.x

    def get_next_obstacle(self, dinoId, obstacles):
        if self.obstacle_in_front_of_dino(self.obstacles[0], self.dinos[dinoId]):
            return obstacles[0]
        else:
            return obstacles[1]

    def get_next_obstacleInfo(dino, next_obstacle, game_speed):

        distance = next_obstacle.x - (dino.x + dino.img.get_width())
        height = next_obstacle.img.get_height()
        width = next_obstacle.img.get_width()
        elevation = settings.FLOOR - (next_obstacle.y + next_obstacle.img.get_height())
        is_cactus = any(next_obstacle.img == cactus for cactus in assets.cactus_img)

        return Obstacle(height, width, distance, elevation, is_cactus)

    def update_dirt(self):
        for dirt in self.floor_dirt:
            dirt.move(self.dino_speed)

    def update_obstacles(self):
        for obst in self.obstacles:
            obst.move(self.dino_speed)

    def update_environment(self):
        self.delete_obstacles_not_visible()
        self.populate_screen_with_obstacles()
        self.update_dirt()
        self.update_obstacles()
        
    def dino_jump(self, dinoIndex):
        self.dinos[dinoIndex].jump()
        
    def dino_duck(self, dinoIndex):
        self.dinos[dinoIndex].duck()

    def update_dino_position(self, dinoIndex):
        self.dinos[dinoIndex].update(self.game_speed)

    def dino_object_collision(self, dinoIndex):
        for obstacle in self.obstacles:
            if mechanics.collision(obstacle, self.dinos[dinoIndex]):
                return True
        return False

    def draw_game(self):
        render.display_floor()
        render.display_score(self.score)
        
        # TODO: Pull out info needed to pass to render?
        # for dino in self.dinos:
        #     dino.draw()
        # for dirt in self.floor_dirt:
        #     dirt.draw()
        # for obst in self.obstacles:
        #     obst.draw()


# TODO: Draw dirt
    # def draw(self):
    #     pygame.draw.circle(
    #         WIN, render.BLACK, (round(self.x), round(self.y)), self.radius
    #     )