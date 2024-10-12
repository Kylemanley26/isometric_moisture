import pygame
import textwrap
from game_settings import WIDTH, HEIGHT, BLACK, WHITE

def fade_effect(screen, text_surface, start_alpha, end_alpha, duration):
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

def show_intro_sequence(screen):
    font = pygame.font.Font(None, 32)
    intro_text = """In 2500, sea level rises had swallowed every continent on Earth underwater. The remains of human civilization live on rugged, floating communities known as atolls, having long forgotten about living on land. A "Dryland" may exist somewhere in the ocean, though some refuse to believe that it does, calling it a myth.

The Mariner, a lone drifter stands on his Trimaran..."""

    wrapped_text = textwrap.fill(intro_text, width=50)
    lines = wrapped_text.split('\n')

    text_surfaces = []
    max_width = 0
    total_height = 0
    for line in lines:
        text_surface = font.render(line, True, WHITE)
        text_surfaces.append(text_surface)
        max_width = max(max_width, text_surface.get_width())
        total_height += text_surface.get_height() + 5  # Add some line spacing

    text_area = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
    y_offset = 0
    for surface in text_surfaces:
        text_area.blit(surface, ((max_width - surface.get_width()) // 2, y_offset))
        y_offset += surface.get_height() + 5  # Add some line spacing

    screen.fill(BLACK)
    
    # Fade in
    fade_effect(screen, text_area, 0, 255, 5000)  # 5 seconds fade in

    # Display text for 5 seconds
    pygame.time.wait(5000)

    # Fade out
    fade_effect(screen, text_area, 255, 0, 5000)  # 5 seconds fade out

    # Ensure the screen is black at the end
    screen.fill(BLACK)
    pygame.display.flip()