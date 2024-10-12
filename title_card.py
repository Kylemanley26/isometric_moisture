import pygame
from game_settings import WIDTH, HEIGHT, BLACK, BLUE, WHITE

def fade_effect(screen, text_surface, start_alpha, end_alpha, duration, interruptible=True):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time
        if elapsed >= duration:
            break

        alpha = start_alpha + (end_alpha - start_alpha) * (elapsed / duration)
        screen.fill(BLACK)
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if interruptible and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                return True  # Indicate that the fade was interrupted

    return False  # Indicate that the fade completed normally

def show_title_card(screen):
    title_font = pygame.font.Font(None, 84)
    subtitle_font = pygame.font.Font(None, 36)

    title_surface = title_font.render("Moist World", True, BLUE)
    subtitle_surface = subtitle_font.render("Embrace the Dampness", True, WHITE)

    combined_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    combined_surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    combined_surface.blit(subtitle_surface, subtitle_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

    screen.fill(BLACK)
    
    # Fade in
    interrupted = fade_effect(screen, combined_surface, 0, 255, 5000)
    
    if not interrupted:
        # Display for 5 seconds
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 5000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    interrupted = True
                    break
            if interrupted:
                break
            pygame.time.wait(100)  # Small wait to prevent busy-waiting

    if not interrupted:
        # Fade out
        fade_effect(screen, combined_surface, 255, 0, 5000)

    # Ensure the screen is black at the end
    screen.fill(BLACK)
    pygame.display.flip()