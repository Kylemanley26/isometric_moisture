import pygame
import random
from game_settings import TILE_SIZE, WATER_FRAMES_PATH, SCREEN_WIDTH, SCREEN_HEIGHT

class Tile:
    def __init__(self, x, y, tile_type):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.type = tile_type

class DynamicObject:
    def __init__(self, x, y, obj_type, image):
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.type = obj_type
        self.image = image

    def update(self):
        # Implement movement or other dynamic behavior here
        pass

class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(x, y, 'water') for y in range(height)] for x in range(width)]
        self.dynamic_objects = []
        self.events = {}  # Dictionary to store events at specific coordinates
        
        self.water_frames = [pygame.image.load(f"{WATER_FRAMES_PATH}/{i:04d}.png") for i in range(40)]
        self.current_water_frame = 0
        
        self.generate_map()

    def generate_map(self):
        # Generate islands, place boats, rafts, etc.
        for _ in range(10):  # Generate 10 small islands
            x = random.randint(0, self.width - 3)
            y = random.randint(0, self.height - 3)
            for dx in range(3):
                for dy in range(3):
                    if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                        self.tiles[x + dx][y + dy].type = 'land'

        # Add some boats and rafts
        boat_image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE))  # Placeholder boat image
        boat_image.fill((139, 69, 19))  # Brown color
        for _ in range(5):
            x = random.randint(0, self.width - 1) * TILE_SIZE
            y = random.randint(0, self.height - 1) * TILE_SIZE
            self.dynamic_objects.append(DynamicObject(x, y, 'boat', boat_image))

    def add_event(self, x, y, event):
        self.events[(x, y)] = event

    def check_event(self, x, y):
        return self.events.get((x, y))

    def update(self):
        # Update water animation
        self.current_water_frame = (self.current_water_frame + 1) % len(self.water_frames)
        
        # Update dynamic objects
        for obj in self.dynamic_objects:
            obj.update()

    def draw(self, screen, camera):
        # Only draw tiles and objects that are within the camera view
        start_x = max(0, camera.x // TILE_SIZE)
        end_x = min(self.width, (camera.x + SCREEN_WIDTH) // TILE_SIZE + 1)
        start_y = max(0, camera.y // TILE_SIZE)
        end_y = min(self.height, (camera.y + SCREEN_HEIGHT) // TILE_SIZE + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.tiles[x][y]
                if tile.type == 'water':
                    screen.blit(self.water_frames[self.current_water_frame], 
                                (tile.rect.x - camera.x, tile.rect.y - camera.y))
                elif tile.type == 'land':
                    pygame.draw.rect(screen, (0, 255, 0), 
                                     (tile.rect.x - camera.x, tile.rect.y - camera.y, TILE_SIZE, TILE_SIZE))

        for obj in self.dynamic_objects:
            if camera.rect.colliderect(obj.rect):
                screen.blit(obj.image, (obj.rect.x - camera.x, obj.rect.y - camera.y))