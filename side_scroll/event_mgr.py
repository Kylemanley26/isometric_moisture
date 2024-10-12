import random
import pygame
from game_settings import WIDTH, HEIGHT, ENEMY_SHIP_IMAGE
from .trader_event import blacksmith_event, shop_event

class Event:
    def __init__(self, name, probability, trigger_distance):
        self.name = name
        self.probability = probability
        self.trigger_distance = trigger_distance

    def check_trigger(self, distance_traveled):
        return (distance_traveled % self.trigger_distance == 0 and 
                random.random() < self.probability)

class EventManager:
    def __init__(self):
        self.events = [
            Event("Whirlpool", 0.2, 1000),
            Event("Kraken", 0.1, 2000),
            Event("Enemy Ship", 0.3, 800),
            Event("Island", 0.4, 1500),
            Event("Shop", 0.3, 1200),
        ]
        self.distance_traveled = 0
        self.pending_event = None
        self.initial_cooldown = 3000

    def update(self, distance_delta):
        self.distance_traveled += distance_delta
        if self.distance_traveled > self.initial_cooldown and not self.pending_event:
            for event in self.events:
                if event.check_trigger(self.distance_traveled):
                    self.pending_event = event.name
                    break
        return self.pending_event

    def clear_pending_event(self):
        self.pending_event = None

def handle_event(screen, event_name, player_ship):
    if event_name == "Enemy Ship":
        from .naval_battle import start_naval_battle, Ship, Weapon
        enemy_ship = generate_random_enemy_ship()
        result = start_naval_battle(screen, player_ship, enemy_ship)
        return result
    elif event_name in ["Whirlpool", "Kraken"]:
        return start_side_scroll_event(screen, event_name)
    elif event_name == "Island":
        return start_exploration_event(screen)
    elif event_name == "Shop":
        return shop_event(screen)
    elif event_name == "Blacksmith":
        return blacksmith_event(screen)
    else:
        print(f"Unknown event: {event_name}")
        return None

def generate_random_enemy_ship():
    from .naval_battle import Ship, Weapon
    
    ship_types = [
        {"name": "Pirate Sloop", "hp": 80, "weapon": Weapon("Cannon", 15, 0.75)},
        {"name": "Merchant Galleon", "hp": 120, "weapon": Weapon("Swivel Gun", 10, 0.9)},
        {"name": "Royal Frigate", "hp": 100, "weapon": Weapon("Long Nine", 20, 0.8)}
    ]
    ship_type = random.choice(ship_types)
    return Ship(ship_type["name"], ship_type["hp"], [ship_type["weapon"]], ENEMY_SHIP_IMAGE)

def start_side_scroll_event(screen, event_name):
    font = pygame.font.Font(None, 48)
    text = font.render(f"Side-scrolling event: {event_name}", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Display for 2 seconds
    return "side_scroll_complete"

def start_exploration_event(screen):
    font = pygame.font.Font(None, 48)
    text = font.render("Exploring island...", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Display for 2 seconds
    return "exploration_complete"

def open_shop(screen):
    font = pygame.font.Font(None, 48)
    text = font.render("Welcome to the shop!", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Display for 2 seconds
    return "shop_visit_complete"