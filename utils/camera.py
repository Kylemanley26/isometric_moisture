import pygame
from game_settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.rect.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - SCREEN_WIDTH), x)  # right
        y = max(-(self.height - SCREEN_HEIGHT), y)  # bottom

        self.rect = pygame.Rect(x, y, self.width, self.height)