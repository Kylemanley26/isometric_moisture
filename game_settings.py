import os

# Screen settings
WIDTH = 800
HEIGHT = 600
SCREEN_WIDTH = WIDTH  # Alias for consistency
SCREEN_HEIGHT = HEIGHT  # Alias for consistency
TITLE = "Moist World"
FPS = 60

# Game settings
TILE_SIZE = 32

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
OCEAN_BLUE = (65, 105, 225)
GRAY = (128, 128, 128)

# Player settings
PLAYER_SPEED = 2

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSET_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSET_DIR, "images")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")

OVERWORLD_DIR = os.path.join(IMAGES_DIR, "overworld")
WATER_FRAMES_PATH = os.path.join(OVERWORLD_DIR, "water_frames")
TRIMARAN_PATH = os.path.join(OVERWORLD_DIR, "trimaran.png")

EVENTS_DIR = os.path.join(IMAGES_DIR, "events")
PLAYER_SHIP_IMAGE = os.path.join(EVENTS_DIR, "player_ship.png")
ENEMY_SHIP_IMAGE = os.path.join(EVENTS_DIR, "enemy_ship.png")

# Ensure all paths exist
for path in [ASSET_DIR, IMAGES_DIR, OVERWORLD_DIR, WATER_FRAMES_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)

# Check if required files exist, if not, print a warning
required_files = [
    os.path.join(IMAGES_DIR, "default_mariner.png"),
    os.path.join(IMAGES_DIR, "character_silhouette.png"),
    TRIMARAN_PATH
]

for file_path in required_files:
    if not os.path.exists(file_path):
        print(f"Warning: Required file {file_path} is missing.")