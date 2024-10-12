import pygame
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_settings import WIDTH, HEIGHT, BLACK, BLUE, WHITE, GRAY

def check_save_file():
    return os.path.exists("save_file.dat")

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.font = pygame.font.Font(None, 32)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.text_color, self.rect, 2)  # Add a border
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.action()
        return False

def new_game():
    return {"action": "start_game"}

def continue_game():
    return {"action": "load_game"}

def open_settings():
    return {"action": "settings"}

def quit_game():
    return {"action": "quit"}

def show_main_menu(screen):
    title_font = pygame.font.Font(None, 64)
    clock = pygame.time.Clock()

    buttons = [
        Button(WIDTH//2 - 100, 200, 200, 50, "Continue" if check_save_file() else "New Game", BLUE, WHITE, continue_game if check_save_file() else new_game),
        Button(WIDTH//2 - 100, 270, 200, 50, "New Game" if check_save_file() else "Settings", BLUE, WHITE, new_game if check_save_file() else open_settings),
        Button(WIDTH//2 - 100, 340, 200, 50, "Settings" if check_save_file() else "Quit", BLUE, WHITE, open_settings if check_save_file() else quit_game),
        Button(WIDTH//2 - 100, 410, 200, 50, "Quit", BLUE, WHITE, quit_game) if check_save_file() else None
    ]
    buttons = [b for b in buttons if b is not None]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"action": "quit"}
            for button in buttons:
                result = button.handle_event(event)
                if result:
                    return result

        screen.fill(BLACK)
        title_surface = title_font.render("Moist World", True, BLUE)
        title_rect = title_surface.get_rect(center=(WIDTH//2, 100))
        screen.blit(title_surface, title_rect)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)