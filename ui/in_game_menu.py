import pygame
from game_settings import WIDTH, HEIGHT, BLACK, WHITE, BLUE, GRAY

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
        return None

def show_in_game_menu(screen):
    menu_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    menu_surface.fill((0, 0, 0, 128))  # Semi-transparent black background

    buttons = [
        Button(WIDTH//2 - 100, 200, 200, 50, "Save", BLUE, WHITE, lambda: {"action": "save"}),
        Button(WIDTH//2 - 100, 260, 200, 50, "Load", BLUE, WHITE, lambda: {"action": "load"}),
        Button(WIDTH//2 - 100, 320, 200, 50, "Settings", BLUE, WHITE, lambda: {"action": "settings"}),
        Button(WIDTH//2 - 100, 380, 200, 50, "Exit to Main", BLUE, WHITE, lambda: {"action": "exit_to_main"}),
        Button(WIDTH//2 - 100, 440, 200, 50, "Exit to Desktop", BLUE, WHITE, lambda: {"action": "exit_to_desktop"})
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"action": "exit_to_desktop"}
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None  # Close the menu without action
            for button in buttons:
                result = button.handle_event(event)
                if result:
                    return result

        screen.blit(menu_surface, (0, 0))
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()