import pygame
import os
from game_settings import WIDTH, HEIGHT, ASSET_DIR, PLAYER_SPEED
from utils.debug_menu import create_debug_menu
from utils.asset_loader import AssetLoader


EVENTS_DIR = os.path.join(ASSET_DIR, "images", "events")
TRADER_SPRITES_DIR = os.path.join(EVENTS_DIR, "trader_sprite")
DEFAULT_MARINER = os.path.join(ASSET_DIR, "images", "default_mariner.png")

def load_image(path):
    try:
        image = pygame.image.load(path).convert_alpha()
        print(f"Successfully loaded image: {path}")
        print(f"Image size: {image.get_size()}")
        return image
    except pygame.error as e:
        print(f"Error: Unable to load image at {path}")
        print(f"Error details: {e}")
        surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        surface.fill((255, 0, 0, 128))
        return surface

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = AssetLoader.load_image(filename)

    def get_image(self, frame, width, height, scale=1):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        if scale != 1:
            image = pygame.transform.scale(image, (width * scale, height * scale))
        return image

class ComplexNPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animations = {
            "idle": self.load_animation("idle.png", 14),
            "idle_2": self.load_animation("idle_2.png", 10),
            "idle_3": self.load_animation("idle_3.png", 10),
            "approval": self.load_animation("approval.png", 8),
            "dialogue": self.load_animation("dialogue.png", 4)
        }
        self.current_animation = "idle"
        self.frame = 0
        self.image = self.animations[self.current_animation][self.frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.idle_index = 0
        #print(f"ComplexNPC initialized at position: {self.rect.topleft}")
        #print(f"Current image size: {self.image.get_size()}")
    
    def set_animation(self, animation_name):
        if animation_name in self.animations:
            self.current_animation = animation_name
            self.frame = 0
        else:
            print(f"Warning: Animation '{animation_name}' not found.")

    def load_animation(self, filename, frame_count):
        full_path = os.path.join(TRADER_SPRITES_DIR, filename)
        sheet = SpriteSheet(full_path)
        animation = []
        sheet_width = sheet.sheet.get_width()
        frame_width = sheet_width // frame_count
        frame_height = sheet.sheet.get_height()
        for i in range(frame_count):
            frame = sheet.get_image(i, frame_width, frame_height, scale=2)  # Adjust scale as needed
            animation.append(frame)
        print(f"Loaded animation '{filename}' with {len(animation)} frames")
        return animation

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            if self.current_animation.startswith("idle"):
                self.idle_index = (self.idle_index + 1) % 3
                self.current_animation = f"idle{'_' + str(self.idle_index + 1) if self.idle_index > 0 else ''}"
            self.frame = (self.frame + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.frame]
            self.animation_timer = 0
        
        # Debug: print current frame and animation
        #print(f"Current animation: {self.current_animation}, Frame: {self.frame}")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(DEFAULT_MARINER)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = PLAYER_SPEED
        print(f"Player initialized at position: {self.rect.topleft}")

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

class ShopUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.items = [
            {"name": "Health Potion", "price": 50},
            {"name": "Sword Upgrade", "price": 100},
            {"name": "Shield", "price": 75}
        ]
        self.selected_item = 0

    def draw(self, screen):
        shop_width, shop_height = WIDTH // 2, HEIGHT // 2
        shop_rect = pygame.Rect((WIDTH - shop_width) // 2, (HEIGHT - shop_height) // 2, shop_width, shop_height)
        pygame.draw.rect(screen, (200, 200, 200), shop_rect)
        pygame.draw.rect(screen, (0, 0, 0), shop_rect, 2)

        for i, item in enumerate(self.items):
            color = (255, 255, 0) if i == self.selected_item else (0, 0, 0)
            text = self.font.render(f"{item['name']} - ${item['price']}", True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, shop_rect.top + 50 + i * 40))
            screen.blit(text, text_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                return self.items[self.selected_item]
        return None


def trader_event(screen, event_type):
    clock = pygame.time.Clock()
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((100, 100, 100))

    player = Player(WIDTH // 4, HEIGHT - 20)
    trader = ComplexNPC(WIDTH * 3 // 4, HEIGHT - 20)
    
    all_sprites = pygame.sprite.Group(player, trader)
    
    shop_ui = ShopUI()
    show_shop = False

    debug_menu = create_debug_menu(screen)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Convert to seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_e:
                    show_shop = not show_shop
                    trader.set_animation("dialogue" if show_shop else "idle")
                elif event.key == pygame.K_BACKQUOTE:
                    debug_menu.toggle()
            
            debug_command = debug_menu.handle_event(event)
            if debug_command:
                return debug_command  # Return the command to trigger the appropriate event

            if show_shop:
                item = shop_ui.handle_input(event)
                if item:
                    print(f"Bought {item['name']} for ${item['price']}")
                    show_shop = False
                    trader.set_animation("approval")

        player.update()
        trader.update(dt)

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        if show_shop:
            shop_ui.draw(screen)

        # Debug: Draw rectangles around sprites
        pygame.draw.rect(screen, (255, 0, 0), player.rect, 1)
        pygame.draw.rect(screen, (0, 255, 0), trader.rect, 1)

        debug_menu.draw()

        pygame.display.flip()

    return "event_complete"

def blacksmith_event(screen):
    return trader_event(screen, "blacksmith")

def shop_event(screen):
    return trader_event(screen, "shop")