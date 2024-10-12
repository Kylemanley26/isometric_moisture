import pygame
import random
from utils.asset_loader import AssetLoader
from game_settings import WIDTH, HEIGHT, FPS, PLAYER_SHIP_IMAGE, ENEMY_SHIP_IMAGE


class Ship:
    def __init__(self, name, max_hp, weapons, image_path):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.weapons = weapons
        self.image = AssetLoader.load_image(image_path)
        # Scale the image to a reasonable size, e.g., 200x200 pixels
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()

class Weapon:
    def __init__(self, name, damage, accuracy):
        self.name = name
        self.damage = damage
        self.accuracy = accuracy

class NavalBattle:
    def __init__(self, player_ship, enemy_ship):
        self.player_ship = player_ship
        self.enemy_ship = enemy_ship
        self.turn = 0

    def player_action(self, action, target):
        if action == "fire":
            self.fire_weapon(self.player_ship, self.enemy_ship, target)

    def enemy_action(self):
        weapon = random.choice(self.enemy_ship.weapons)
        self.fire_weapon(self.enemy_ship, self.player_ship, weapon)

    def fire_weapon(self, attacker, defender, weapon):
        if random.random() < weapon.accuracy:
            defender.current_hp -= weapon.damage
            print(f"{attacker.name} hit {defender.name} for {weapon.damage} damage!")
        else:
            print(f"{attacker.name} missed!")

    def is_game_over(self):
        return self.player_ship.current_hp <= 0 or self.enemy_ship.current_hp <= 0

    def draw(self, screen):
        font = pygame.font.Font(None, 24)
        
        # Draw player ship
        screen.blit(self.player_ship.image, (50, 100))
        
        # Draw enemy ship
        screen.blit(self.enemy_ship.image, (WIDTH - 250, 100))
        
        # Draw health bars
        pygame.draw.rect(screen, (255, 0, 0), (50, HEIGHT - 50, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (50, HEIGHT - 50, 200 * (self.player_ship.current_hp / self.player_ship.max_hp), 20))
        
        pygame.draw.rect(screen, (255, 0, 0), (WIDTH - 250, HEIGHT - 50, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (WIDTH - 250, HEIGHT - 50, 200 * (self.enemy_ship.current_hp / self.enemy_ship.max_hp), 20))
        
        # Draw ship names and HP
        player_info = font.render(f"{self.player_ship.name}: {self.player_ship.current_hp}/{self.player_ship.max_hp} HP", True, (255, 255, 255))
        enemy_info = font.render(f"{self.enemy_ship.name}: {self.enemy_ship.current_hp}/{self.enemy_ship.max_hp} HP", True, (255, 255, 255))
        screen.blit(player_info, (50, HEIGHT - 80))
        screen.blit(enemy_info, (WIDTH - 250, HEIGHT - 80))

def start_naval_battle(screen, player_ship, enemy_ship):
    battle = NavalBattle(player_ship, enemy_ship)
    clock = pygame.time.Clock()

    while not battle.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                # For simplicity, let's say left click fires the first weapon
                if event.button == 1:
                    battle.player_action("fire", player_ship.weapons[0])
                    battle.enemy_action()

        screen.fill((0, 0, 0))  # Clear screen
        battle.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    return "player" if enemy_ship.current_hp <= 0 else "enemy"