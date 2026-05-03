# settings.py
# Game constants and configuration

WIDTH = 480
HEIGHT = 640
FPS = 60
TITLE = 'Space Shooter (Beginner Friendly)'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (10, 10, 30)

# Player settings
PLAYER_SPEED = 300  # pixels per second
PLAYER_LIVES = 3

# Bullet settings
BULLET_SPEED = -500  # negative = up

# Enemy settings
ENEMY_SPEED_MIN = 80
ENEMY_SPEED_MAX = 150
ENEMY_SPAWN_DELAY = 1.0  # seconds between spawns (will get faster)

# Assets
ASSETS_DIR = 'assets'
IMAGES_DIR = ASSETS_DIR + '/images'
SOUNDS_DIR = ASSETS_DIR + '/sounds'
