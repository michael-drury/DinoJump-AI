import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FLOOR_OFFSET = 20


class Render:
    def __init__(self, game_title, window_width, window_height, floor_height):

        if not game_title and type(game_title) is str:
            raise ValueError("Title cannot be empty")

        self.win_width = window_width
        self.win_height = window_height
        self.floor_height = floor_height
        pygame.init()
        self.font = pygame.font.SysFont("arial", 30)
        self.window = pygame.display.set_mode((window_width, window_height))
        pygame.font.init()
        pygame.display.set_caption(game_title)

    def close_window(self):
        pygame.quit()

    def display_score(self, score):
        text_surface = self.font.render(
            "Score: {}".format(round(score, 2)), True, BLACK
        )
        text_rect = text_surface.get_rect()
        text_rect.bottom = self.win_height - 20
        text_rect.left = 20
        self.window.blit(text_surface, text_rect)

    def display_generation(self, generation):
        if type(generation) is not int:
            raise TypeError("Generation must be of type int")

        text_surface = self.font.render("Gen: {}".format(generation), True, BLACK)
        self.window.blit(text_surface, (10, 10))

    def display_floor(self):
        pygame.draw.rect(
            self.window, BLACK, (0, self.floor_height - FLOOR_OFFSET, self.win_width, 2)
        )

    def set_background_white(self):
        self.window.fill(WHITE)

    def draw_img(self, file, posX, posY):
        self.window.blit(file, (posX, posY))

    def draw_circle(self, radius, pos_x, pos_y):
        pygame.draw.circle(self.window, BLACK, (pos_x, pos_y), radius)

    def update_display(self):
        pygame.display.update()
