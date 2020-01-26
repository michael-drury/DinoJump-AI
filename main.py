"""
Genetic algorithm NEAT plays a version of the dinosaur jump game from google.

The game has been written in Python, and created using the Pygame module.
NOTE: Pygame module uses top left coordinate as origin (0, 0)


Date Modified: 24th January 2020
Author: Michael Drury
"""

import os
import pygame
import random
import neat
import visualize

# Adjustable Game Variables
WIN_WIDTH = 1200
WIN_HEIGHT = 400
FLOOR = 350  # y location of dinosaur in game window
FRAME_RATE = 60
IMG_SPEED = FRAME_RATE / 10  # Speed of character animation (i.e. no. of frames between image change)
INITIAL_GAME_SPEED = 8  # Set speed of oncoming objects

# Global Variables
game_speed = INITIAL_GAME_SPEED
generation = 0  # Current generation of neural nets
score = 0  # Game score of the remaining current generation of neural nets

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialise Pygame module
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("arial", 30)  # Select font type and size
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # Setup game window
pygame.display.set_caption("Dino Jump")
clock = pygame.time.Clock()  # Create clock to limit game speed

# Import images
dino_run_img = [pygame.image.load(os.path.join("images", "dino_run_" + str(x) + ".png")) for x in range(2)]
dino_duck_img = [pygame.image.load(os.path.join("images", "dino_duck_" + str(x) + ".png")) for x in range(2)]
dino_jump_img = pygame.image.load(os.path.join("images", "dino_jump.png"))
bird_img = [pygame.image.load(os.path.join("images", "bird_" + str(x) + ".png")) for x in range(2)]
cactus_img = [pygame.image.load(os.path.join("images", "cactus_" + str(x) + ".png")) for x in range(3)]


class Dino:
    def __init__(self):
        self.img = dino_run_img[0]
        self.x = 100
        self.y = FLOOR - self.img.get_height()
        self.ducking = False
        self.jumping = False
        self.jump_count = 0
        self.jump_velocity = 100  # Initial velocity of jump
        self.gravity = -400  # Acceleration due to gravity
        self.img_count = IMG_SPEED  # Set img_count to the start of its loop

    def jump(self, is_jumping):
        self.img = dino_jump_img
        self.jumping = is_jumping

    def duck(self, is_ducking):
        if is_ducking:
            self.gravity = -600  # Increase gravity when ducking key pressed to quickly reach floor when jumping
        else:
            self.gravity = -400  # Return gravity to its original value when duck key is not pressed
        self.ducking = is_ducking
        self.img_count = IMG_SPEED

    def move(self):
        # If the dino is set to jump or yet to complete a jump...
        if self.jumping or (self.jump_count != 0):
            self.jump_count += 1
            time = self.jump_count / FRAME_RATE  # Calculate time increment per frame
            # Use newtonian motion equation to determine dino height (s = ut + 0.5 * a * t^2)
            self.y += -self.jump_velocity * time + 0.5 * -self.gravity * time ** 2
            # If the dino touches the floor, stop jumping
            if self.y >= FLOOR - self.img.get_height():
                self.y = FLOOR - self.img.get_height()
                self.jump_count = 0
                self.img_count = IMG_SPEED

    def run(self, image):
        self.y = FLOOR - image[0].get_height()
        animate(self, image)

    def draw(self):
        # If the jump key is not pressed and dino is not currently jumping...
        if (not self.jumping) and (self.jump_count == 0):
            if self.ducking:
                self.run(dino_duck_img)
            else:
                self.run(dino_run_img)

        WIN.blit(self.img, (self.x, self.y))  # Copy image to game window


class Obstacles:
    def __init__(self, x):
        self.x = x
        self.y = None
        self.img = None

    def move(self):
        global game_speed
        self.x -= game_speed

    def _draw(self):
        WIN.blit(self.img, (self.x, self.y))

    # Return true if collision detected between dino and obstacle
    def collision(self, dino):
        dino_mask = get_mask(dino.img)
        obstacle_mask = get_mask(self.img)
        offset = (round(self.x - dino.x), round(self.y - dino.y))

        if dino_mask.overlap(obstacle_mask, offset):
            return True
        return False


class Cactus(Obstacles):
    def __init__(self, x, size):
        super().__init__(x)
        self.img = cactus_img[size]
        self.y = FLOOR - self.img.get_height()

    def draw(self):
        self._draw()


class Bird(Obstacles):
    def __init__(self, x):
        super().__init__(x)
        self.img = bird_img[1]
        self.y = FLOOR - 90 * random.randint(1, 3)  # Randomly select bird height from 3 levels
        self.img_count = 0  # Image count to enable animation bird wings

    def draw(self):
        animate(self, bird_img)
        self._draw()


class Dirt:
    def __init__(self, x):
        self.x = x
        self.y = FLOOR - 15 + random.randint(0, 30)
        self.radius = random.randint(0, 4)

    def draw(self):
        pygame.draw.circle(WIN, BLACK, (round(self.x), round(self.y)), self.radius)

    def move(self):
        global game_speed
        self.x -= game_speed
        if self.x < -self.radius:
            self.x = WIN_WIDTH + self.radius


# Return image mask indicating where pixels exist within the containing rectangle
def get_mask(image):
    return pygame.mask.from_surface(image)


# Swap sprite image at fixed rate to animate characters
def animate(obj, image):
    if obj.img_count == IMG_SPEED:
        obj.img = image[0]
    elif obj.img_count == 2 * IMG_SPEED:
        obj.img = image[1]
        obj.img_count = -1
    obj.img_count += 1


# Draw the window and all game objects/ text
def draw_window(dinos, floor_dirt, obstacles):
    WIN.fill(WHITE)  # Set game background to white

    # Draw all moving game objects
    for dino in dinos:
        dino.draw()
    for dirt in floor_dirt:
        dirt.draw()
    for obst in obstacles:
        obst.draw()

    # Display Score
    text_surface = FONT.render("Score: {}".format(round(score, 2)), True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.bottom = WIN_HEIGHT - 20
    text_rect.left = 20
    WIN.blit(text_surface, text_rect)

    # Display Generation
    text_surface = FONT.render("Gen: {}".format(generation), True, BLACK)
    WIN.blit(text_surface, (10, 10))

    # Draw a line across the game window to show the floor
    pygame.draw.rect(WIN, BLACK, (0, FLOOR - 20, WIN_WIDTH, 2))
    pygame.display.update()


# Get genomes to play the Dino Jump game
def eval_genomes(genomes, config):
    global game_speed
    global generation
    global score

    game_speed = INITIAL_GAME_SPEED  # Reset game speed
    score = 0  # Reset score after each game
    generation += 1  # Increment generation after each game

    # Create empty list of nets, genomes and dinos
    nets = []
    ge = []
    dinos = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)  # Generate neural networks
        nets.append(net)
        dinos.append(Dino())  # Generate dinos to be controlled by neural networks
        g.fitness = 0
        ge.append(g)

    # Generate floor dirt at fixed intervals across game window
    floor_dirt = []
    for i in range(20):
        dirt_x = i * (WIN_WIDTH / 20)
        floor_dirt.append(Dirt(int(dirt_x)))

    obstacles = []  # Create empty list of obstacles

    run_game = True
    #  ---------------------------- Main game loop ----------------------------  #
    while run_game:
        clock.tick(FRAME_RATE)  # Restrict game speed to operate at specified frame rate
        game_speed += 0.03/FRAME_RATE  # Increment the game speed each game loop

        # If the red x button in the top left of game window is pressed, quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # If all the dinos have been eliminated from the game, quit the game
        if len(dinos) <= 0:
            run_game = False

        for obst in obstacles:
            if obst.x < -obst.img.get_width():  # If obstacle goes off the screen
                obstacles.pop(0)  # Remove obstacle

        # While there are less than three obstacles, populate the game with additional obstacles
        while len(obstacles) != 3:
            # Generate a random new obstacle (0.25 chance of getting specific cactus type or bird)
            rand_num = random.randint(0, 3)
            if obstacles:
                x_pos = obstacles[-1].x + random.randint(400, 600)  # Randomise distance between obstacles
            else:
                x_pos = WIN_WIDTH + 50
            if rand_num == 3:
                obstacles.append(Bird(x_pos))
            else:
                obstacles.append(Cactus(x_pos, rand_num))

        for x, dino in enumerate(dinos):
            dino.move()
            ge[x].fitness += 0.1  # Increase fitness of genomes for dinos that have not yet been eliminated

            # Determine next object dino has to jump over
            if obstacles[0].x + obstacles[0].img.get_width() > dino.x:  # If the obstacle is in front of the dino...
                next_obstacle = obstacles[0]  # Set next obstacle to obstacle in list furthest to left
            else:  # i.e.) If an obstacle is behind the dino...
                next_obstacle = obstacles[1]  # Set next obstacle to obstacle second from the left

            # Get neuron input values
            obst_dist = next_obstacle.x - (dino.x + dino.img.get_width())
            obst_height = next_obstacle.img.get_height()
            obst_width = next_obstacle.img.get_width()
            obst_y = FLOOR - (next_obstacle.y + next_obstacle.img.get_height())
            is_cactus = 0
            for cactus in cactus_img:
                if next_obstacle.img == cactus:
                    is_cactus = 1
            dino_height = FLOOR - dino.y

            # Calculate output neurons from specified input neurons
            output = nets[x].activate((obst_dist, obst_height, obst_width, obst_y, game_speed, dino_height, is_cactus))

            # Trigger jump or duck keys depending on output neurons
            if output[0] > 0.5:
                dino.jump(True)
            else:
                dino.jump(False)

            if output[1] > 0.5:
                dino.duck(True)
            else:
                dino.duck(False)

        for dirt in floor_dirt:
            dirt.move()

        for obst in obstacles:
            obst.move()
            # Collision detection
            for x, dino in enumerate(dinos):
                if obst.collision(dino):
                    ge[x].fitness -= 1  # Remove 1 from fitness score when hits an object
                    # Remove dinos and their corresponding networks if they have a collision
                    dinos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

        score += 1  # Increase score if any dinos are remaining

        draw_window(dinos, floor_dirt, obstacles)


# Configure NEAT and implement genetic algorithm to determine optimal neural network to play the game
def run(config_file):
    # Load configuration file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    p = neat.Population(config)

    # Report genome statistics
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Determine optimal neural network
    winner = p.run(eval_genomes, 100)  # Evolve 100 generations

    # Plot/print the most successful neural network
    node_names = {-1: 'obst_dist', -2: 'obst_height', -3: 'obst_width', -4: 'obst_y', -5: 'game_speed', -6: 'dino.y',
                  -7: 'is_cactus', 0: 'Jump', 1: 'Duck'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Load the configuration file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    # Run algorithm using configuration file
    run(config_path)
