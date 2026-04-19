# Game settings
TITLE = "Tank Game"

WIDTH = 1280
HEIGHT = 720

FPS = 60

# Basic colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
TAN = (234, 219, 198)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Player/Tank
TANKSCALE = 0.75
TANK_HEALTH = 3
TANK_COLOURS = {1: "Blue", 2: "Red"}
BLUE_TANK_SPRITE_PATH = 'Assets/BlueTank.png'
BLUE_BULLET_SPRITE_PATH = 'Assets/BlueBullet.png'
RED_TANK_SPRITE_PATH = 'Assets/RedTank.png'
RED_BULLET_SPRITE_PATH = 'Assets/RedBullet.png'
MOVE_COOLDOWN = 30

# Bullet/shooting
SHOOT_COOLDOWN = 20
BULLET_SCALE = 1
BULLET_SPEED = 5
BULLET_LIFETIME = 5

# grid
BACKGROUND_IMAGE = 'Assets/Maps/BasicTestBackground.png'
MAP_FILENAME = 'Assets/Maps/TextMap.txt'
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# ui elements
BLUETANK_HEALTH_X = 100
BLUETANK_HEALTH_Y = 100
HEART_SCALE = 2
