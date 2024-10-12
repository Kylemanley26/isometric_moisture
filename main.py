import pygame
from game_settings import WIDTH, HEIGHT, TITLE, FPS, PLAYER_SHIP_IMAGE
from overworld.overworld_map import OverworldMap
from ui.main_menu import show_main_menu
from ui.in_game_menu import show_in_game_menu
from title_card import show_title_card
from intro_sequence import show_intro_sequence
from mariner_creation import create_mariner
from side_scroll.naval_battle import Ship, Weapon, start_naval_battle
from side_scroll.event_mgr import handle_event, generate_random_enemy_ship
from side_scroll.trader_event import shop_event, blacksmith_event
from utils.debug_menu import create_debug_menu
from utils.asset_loader import AssetLoader


def start_exploration_event(screen):
    font = pygame.font.Font(None, 48)
    text = font.render("Exploring island...", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Display for 2 seconds

def start_side_scroll_event(screen, event_name):
    font = pygame.font.Font(None, 48)
    text = font.render(f"Side-scrolling event: {event_name}", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Display for 2 seconds

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Show the title card
    show_title_card(screen)
    
    while True:
        # Show the main menu
        menu_result = show_main_menu(screen)
        
        if menu_result["action"] == "quit":
            break
        elif menu_result["action"] == "start_game":
            # Show the intro sequence
            show_intro_sequence(screen)
            
            # Create the mariner
            mariner = create_mariner(screen)
            
            if mariner:
                # Create player ship
                player_ship = Ship(mariner['name'], 100, [Weapon("Cannon", 20, 0.8)], PLAYER_SHIP_IMAGE)
                
                # Start the game
                overworld = OverworldMap()
                debug_menu = create_debug_menu(screen)
                
                running = True
                while running:
                    dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                menu_result = show_in_game_menu(screen)
                                if menu_result:
                                    if menu_result["action"] == "exit_to_main":
                                        running = False
                                    elif menu_result["action"] == "exit_to_desktop":
                                        return
                            elif event.key == pygame.K_BACKQUOTE:
                                debug_menu.toggle()

                        debug_command = debug_menu.handle_event(event)
                        if debug_command:
                            handle_debug_command(screen, debug_command, player_ship)

                    overworld.update(dt)
                    
                    if overworld.pending_event:
                        result = handle_event(screen, overworld.pending_event, player_ship)
                        overworld.event_manager.clear_pending_event()
                        if result == "event_complete":
                            # Event handled, continue with the game
                            pass
                        elif result == "exit_event":
                            # Player chose to exit the event
                            pass

                    overworld.draw(screen)
                    debug_menu.draw()
                    
                    pygame.display.flip()

        elif menu_result["action"] == "load_game":
            # Implement load game functionality
            pass
        elif menu_result["action"] == "settings":
            # Implement settings menu
            pass

    pygame.quit()

def handle_debug_command(screen, command, player_ship):
    if command == "shop":
        shop_event(screen)
    elif command == "battle":
        enemy_ship = generate_random_enemy_ship()
        start_naval_battle(screen, player_ship, enemy_ship)
    elif command == "island":
        start_exploration_event(screen)
    elif command in ["whirl", "kraken"]:
        start_side_scroll_event(screen, "Whirlpool" if command == "whirl" else "Kraken")

if __name__ == "__main__":
    main()