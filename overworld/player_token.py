import pygame
from game_settings import WIDTH, HEIGHT, PLAYER_SPEED, TRIMARAN_PATH

class PlayerToken(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def load_image(self):
        try:
            return pygame.image.load(TRIMARAN_PATH).convert_alpha()
        except pygame.error:
            print(f"Unable to load player image: {TRIMARAN_PATH}")
            surface = pygame.Surface((50, 50))
            surface.fill((255, 0, 0))  # Red color as placeholder
            return surface

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED

        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, self.rect)