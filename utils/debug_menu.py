import pygame

class DebugMenu:
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.font = pygame.font.Font(None, 24)
        self.input_text = ""
        self.commands = {
            "shop": "Trigger shop event",
            "battle": "Trigger naval battle event",
            "island": "Trigger island exploration event",
            "whirl": "Trigger whirlpool event",
            "kraken": "Trigger kraken event",
            "help": "Show this help message"
        }

    def toggle(self):
        self.active = not self.active
        self.input_text = ""

    def handle_event(self, event):
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:
                self.toggle()
            elif event.key == pygame.K_RETURN:
                command = self.input_text.strip().lower()
                self.input_text = ""
                return self.process_command(command)
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

        return None

    def process_command(self, command):
        if command in self.commands:
            if command == "help":
                self.show_help()
                return None
            return command
        else:
            print(f"Unknown command: {command}")
            return None

    def show_help(self):
        print("Available commands:")
        for cmd, desc in self.commands.items():
            print(f"{cmd}: {desc}")

    def draw(self):
        if not self.active:
            return

        # Draw semi-transparent background
        overlay = pygame.Surface((self.screen.get_width(), 30))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw input text
        text_surface = self.font.render(f"> {self.input_text}", True, (255, 255, 255))
        self.screen.blit(text_surface, (5, 5))

def create_debug_menu(screen):
    return DebugMenu(screen)