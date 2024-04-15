import pygame


def get_pixel_locations(image):
    return pygame.mask.from_surface(image)


def collision(img1, x1, y1, img2, x2, y2):
    mask1 = get_pixel_locations(img1)
    mask2 = get_pixel_locations(img2)
    offset = (round(x2 - x1), round(y2 - y1))

    return mask1.overlap(mask2, offset)
