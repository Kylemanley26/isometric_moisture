import pygame
from game_settings import WIDTH, HEIGHT, BLACK, WHITE

def main_game_loop(screen, mariner):
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Return to main menu on ESC key

        # Clear the screen
        screen.fill(BLACK)

        # Display mariner info
        text = font.render(f"Mariner: {mariner['name']} - Press ESC to return to menu", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS