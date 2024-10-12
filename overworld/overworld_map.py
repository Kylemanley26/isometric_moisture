import pygame
import sys
import os
import random


# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#directory imports
from game_settings import WIDTH, HEIGHT, OCEAN_BLUE, WATER_FRAMES_PATH, TRIMARAN_PATH, FPS, PLAYER_SPEED
from side_scroll.event_mgr import EventManager, handle_event

class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.width = width
        self.height = height

    def apply(self, entity_rect):
        return entity_rect.move(self.rect.topleft)

    def update(self, target_rect):
        x = -target_rect.centerx + int(WIDTH / 2)
        y = -target_rect.centery + int(HEIGHT / 2)

        # Limit scrolling to map size
        x = max(-(self.width - WIDTH), min(0, x))
        y = max(-(self.height - HEIGHT), min(0, y))

        self.rect.topleft = (x, y)

class Wake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = (255, 255, 255, 200)  # White with some transparency
        self.life = 60  # Number of frames the wake particle will live for

    def update(self):
        self.life -= 1
        self.size = max(0, self.size - 0.1)  # Gradually decrease size
        self.color = (255, 255, 255, max(0, self.color[3] - 3))  # Fade out

    def draw(self, screen, camera):
        pos = camera.apply(pygame.Rect(self.x, self.y, self.size, self.size))
        pygame.draw.circle(screen, self.color, pos.center, int(self.size))

class OverworldMap:
    def __init__(self):
        self.frame_index = 0
        self.water_frames = []
        self.wake_particles = []
        self.event_manager = EventManager()
        self.total_distance_traveled = 0
        self.pending_event = None
        self.distance_traveled = 0

        # Load water frames
        for i in range(40):
            frame_path = os.path.join(WATER_FRAMES_PATH, f"{i:04d}.png")
            if os.path.exists(frame_path):
                frame = pygame.image.load(frame_path).convert()
                frame = pygame.transform.scale(frame, (WIDTH, HEIGHT))  # Scale to screen size
                self.water_frames.append(frame)
            else:
                print(f"Warning: {frame_path} does not exist.")
        
        if not self.water_frames:
            print("No water frames loaded. Creating a default blue background.")
            default_bg = pygame.Surface((WIDTH, HEIGHT))
            default_bg.fill(OCEAN_BLUE)
            self.water_frames = [default_bg]
        
        # Load trimaran sprite sheet
        self.trimaran_sheet = self.load_image(TRIMARAN_PATH)

        # Load trimaran-full sprite sheet
        trimaran_full_path = os.path.join(os.path.dirname(TRIMARAN_PATH), "trimaran-full.png")
        self.trimaran_full_sheet = self.load_image(trimaran_full_path)

        # Extract frames from both sprite sheets
        self.trimaran_frames = self.extract_frames(self.trimaran_sheet)
        self.trimaran_full_frames = self.extract_frames(self.trimaran_full_sheet)

        self.trimaran_rect = self.trimaran_frames[0].get_rect()
        self.trimaran_rect.center = (WIDTH // 2, HEIGHT // 2)

        self.direction = 'right'
        self.moving = False
        self.sailing = False

        # Map dimensions
        self.map_width = WIDTH * 3
        self.map_height = HEIGHT * 3
        self.camera = Camera(self.map_width, self.map_height)

        # For controlling water animation speed
        self.frame_delay = FPS // 10
        self.frame_counter = 0

        # Remove island generation for now
        self.islands = []

    def load_image(self, path):
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error:
            print(f"Error: Unable to load image at {path}")
            surface = pygame.Surface((200, 50))
            surface.fill((255, 0, 0))
            return surface

    def extract_frames(self, sheet):
        frames = []
        frame_width = sheet.get_width() // 4
        frame_height = sheet.get_height() // 2
        for y in range(2):
            for x in range(4):
                frame = sheet.subsurface((x * frame_width, y * frame_height, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.moving = False
        old_pos = self.trimaran_rect.center

        if keys[pygame.K_LEFT]:
            self.trimaran_rect.x -= PLAYER_SPEED
            self.direction = 'left'
            self.moving = True
        elif keys[pygame.K_RIGHT]:
            self.trimaran_rect.x += PLAYER_SPEED
            self.direction = 'right'
            self.moving = True
        elif keys[pygame.K_UP]:
            self.trimaran_rect.y -= PLAYER_SPEED
            self.direction = 'up'
            self.moving = True
        elif keys[pygame.K_DOWN]:
            self.trimaran_rect.y += PLAYER_SPEED
            self.direction = 'down'
            self.moving = True
       
        # Toggle sailing mode with spacebar
        if keys[pygame.K_SPACE]:
            self.sailing = not self.sailing

        # Keep the trimaran within the map bounds
        self.trimaran_rect.clamp_ip(pygame.Rect(0, 0, self.map_width, self.map_height))
        
        # Calculate distance traveled for event triggering
        distance_delta = ((self.trimaran_rect.centerx - old_pos[0])**2 + 
                          (self.trimaran_rect.centery - old_pos[1])**2)**0.5
        self.total_distance_traveled += distance_delta

        #self.pending_event = self.event_manager.update(distance_delta)
        #distance_delta = ((self.player.rect.centerx - self.player.old_position[0])**2 + 
        #                  (self.player.rect.centery - self.player.old_position[1])**2)**0.5
        #self.distance_traveled += distance_delta
        

        # Create wake particles if moving
        if self.moving:
            wake_x, wake_y = old_pos
            if self.direction == 'left':
                wake_x += self.trimaran_rect.width // 2
            elif self.direction == 'right':
                wake_x -= self.trimaran_rect.width // 2
            elif self.direction == 'up':
                wake_y += self.trimaran_rect.height // 2
            elif self.direction == 'down':
                wake_y -= self.trimaran_rect.height // 2
            
            self.wake_particles.append(Wake(wake_x, wake_y))

        # Update wake particles
        for particle in self.wake_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.wake_particles.remove(particle)

        # Update camera
        self.camera.update(self.trimaran_rect)

        # Update water animation
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.water_frames)
            self.frame_counter = 0

        # Update EventManager and check for pending events
        self.pending_event = self.event_manager.update(distance_delta)
        self.pending_event = self.event_manager.update(self.distance_traveled)

    def get_trimaran_frame(self):
        frame_index = 0
        if self.direction == 'left':
            frame_index = 0
        elif self.direction == 'down':
            frame_index = 1
        elif self.direction == 'right':
            frame_index = 2
        elif self.direction == 'up':
            frame_index = 5

        if self.sailing:
            return self.trimaran_full_frames[frame_index]
        else:
            return self.trimaran_frames[frame_index]

    def draw(self, screen):
        # Draw the water background
        screen.blit(self.water_frames[self.frame_index], (0, 0))

        # Draw wake particles
        for particle in self.wake_particles:
            particle.draw(screen, self.camera)
        
        # Draw the trimaran
        trimaran_screen_pos = self.camera.apply(self.trimaran_rect)
        current_frame = self.get_trimaran_frame()
        screen.blit(current_frame, trimaran_screen_pos)

        if self.pending_event:
            font = pygame.font.Font(None, 36)
            event_text = f"Event: {self.pending_event}! Press E to engage."
            event_surface = font.render(event_text, True, (255, 255, 0))
            screen.blit(event_surface, (WIDTH // 2 - event_surface.get_width() // 2, 50))

        # Draw debug information including total distance traveled
        font = pygame.font.Font(None, 24)
        debug_info = f"Trimaran pos: {self.trimaran_rect.topleft}, Camera pos: {self.camera.rect.topleft}, Direction: {self.direction}, Sailing: {self.sailing}, Distance: {self.total_distance_traveled:.2f}"
        debug_surface = font.render(debug_info, True, (255, 255, 255))
        screen.blit(debug_surface, (10, 10))


def main_game_loop(screen):
    overworld = OverworldMap()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and overworld.pending_event:
                    handle_event(screen, overworld.pending_event)
                    overworld.event_manager.clear_pending_event()

        overworld.update()
        overworld.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)