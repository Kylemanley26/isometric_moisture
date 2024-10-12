import pygame
import os
from game_settings import IMAGES_DIR

class AssetLoader:
    @staticmethod
    def load_image(filename, scale=1, convert_alpha=True):
        try:
            path = os.path.join(IMAGES_DIR, filename)
            print(f"Attempting to load image from: {path}")  # Debug print
            image = pygame.image.load(path)
            if convert_alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
            if scale != 1:
                new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, new_size)
            return image
        except pygame.error as e:
            print(f"Error loading image {filename}: {e}")
            # Create a colored rectangle as a placeholder
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            surface.fill((255, 0, 0, 128))  # Semi-transparent red
            return surface

    #@staticmethod
    #def load_sound(filename):
    #    try:
    #        path = os.path.join(IMAGES_DIR, filename)
    #        return pygame.mixer.Sound(path)
    #    except pygame.error as e:
    #        print(f"Error loading sound {filename}: {e}")
    #        return None