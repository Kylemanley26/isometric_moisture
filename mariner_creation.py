import pygame
import os
from game_settings import WIDTH, HEIGHT, BLACK, WHITE, BLUE, IMAGES_DIR, WATER_FRAMES_PATH

def scale_image(image, target_height):
    aspect_ratio = image.get_width() / image.get_height()
    new_width = int(target_height * aspect_ratio)
    return pygame.transform.scale(image, (new_width, target_height))

def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error:
        print(f"Error: Unable to load image at {path}")
        # Create a colored rectangle as a placeholder
        surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        surface.fill((255, 0, 0, 128))  # Semi-transparent red
        return surface

def create_mariner(screen):
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Load and scale sprites
    default_sprite = load_image(os.path.join(IMAGES_DIR, 'default_mariner.png'))
    silhouette = load_image(os.path.join(IMAGES_DIR, 'character_silhouette.png'))

    # Scale images to a consistent height
    target_height = int(HEIGHT * 0.6)  # 60% of screen height
    default_sprite = scale_image(default_sprite, target_height)
    silhouette = scale_image(silhouette, target_height)

    # Character data
    characters = [
        {"name": "Default Mariner", "sprite": default_sprite, "locked": False},
        {"name": "????", "sprite": silhouette, "locked": True},
        {"name": "????", "sprite": silhouette, "locked": True}
    ]

    selected_index = 0
    
    # Load background image
    background = load_image(os.path.join(WATER_FRAMES_PATH, '0000.png'))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    creating = True
    while creating:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(characters)
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(characters)
                elif event.key == pygame.K_RETURN:
                    if not characters[selected_index]["locked"]:
                        return {"name": characters[selected_index]["name"]}
                elif event.key == pygame.K_ESCAPE:
                    return None

        screen.fill(BLACK)
        screen.blit(background, (0, 0))

        # Calculate positions
        total_width = sum(char["sprite"].get_width() for char in characters)
        spacing = (WIDTH - total_width) // (len(characters) + 1)
        current_x = spacing

        # Draw character sprites
        for i, character in enumerate(characters):
            sprite_rect = character["sprite"].get_rect()
            sprite_rect.centerx = current_x + sprite_rect.width // 2
            sprite_rect.centery = HEIGHT // 2  # Center vertically
            
            screen.blit(character["sprite"], sprite_rect)
            
            # Draw selection indicator
            if i == selected_index:
                pygame.draw.rect(screen, BLUE, sprite_rect, 3)
            
            # Draw character name
            name_text = font.render(character["name"], True, WHITE)
            name_rect = name_text.get_rect(centerx=sprite_rect.centerx, top=sprite_rect.bottom + 10)
            screen.blit(name_text, name_rect)

            current_x += sprite_rect.width + spacing

        # Draw instructions
        instructions = font.render("Use LEFT/RIGHT arrows to select, ENTER to confirm", True, WHITE)
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(instructions, instructions_rect)

        pygame.display.flip()
        clock.tick(60)

    return None