import pygame


def get_pixel_locations(image):
    return pygame.mask.from_surface(image)


def collision(obstacle, dino):
    dino_mask = get_pixel_locations(dino.img)
    obstacle_mask = get_pixel_locations(obstacle.img)
    offset = (round(obstacle.x - dino.x), round(obstacle.y - dino.y))

    return dino_mask.overlap(obstacle_mask, offset)
