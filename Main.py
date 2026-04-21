import pygame
import sys

from os import path
from PIL import Image, ImageDraw

from Obstacles import Wall
from Settings import *
from Player import Player
from AITank import AITank
from TileMap import Map

# resources
# https://www.youtube.com/watch?v=8-hNcOmkZtg
# https://www.youtube.com/watch?v=wu1cd1Qycz4&t=3s
# https://www.youtube.com/watch?v=PfxwNxXveQk
# https://www.redblobgames.com/pathfinding/a-star/implementation.html
# https://python-course.eu/applications-python/finite-state-machine.php
# https://www.geeksforgeeks.org/python/create-and-save-animated-gif-with-python-pillow/
# https://www.youtube.com/watch?v=lecAm3eYCeY
# https://www.pygame.org/docs/ref/image.html#pygame.image.tostring

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # set the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        # Load Assets
        self.background = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE).convert(), (WIDTH, HEIGHT))

        # game control
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 10)

        self.load()
        self.wall_positions = []
        # self.paused = False

        # gif variables
        self.images = []
        self.image_cooldown = IMAGE_COOLDOWN

    # runs when the game loads
    def load(self):
        game_dir = path.dirname(__file__)
        self.map = Map(path.join(game_dir, MAP_FILENAME))

    def new_instance(self):
        # create a new instance of the game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()

        # create sprites
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '*':
                    Wall(self, col, row)
                    self.wall_positions.append((col, row))
                elif tile == 'P':
                    self.player = Player(self, col, row, 1, BLUETANK_HEALTH_X)
                elif tile == 'T':
                    self.ai_tank1 = AITank(self, col, row, 2, RED_TANK_SPRITE_PATH, RED, RED_BULLET_SPRITE_PATH, 2, 6, REDTANK_HEALTH_X, 3, 3)
                elif tile == 'L':
                    self.ai_tank2 = AITank(self, col, row, 3, GREEN_TANK_SPRITE_PATH, GREEN, GREEN_BULLET_SPRITE_PATH, 1, 7, BLUETANK_HEALTH_X, 5, 6)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update items in the game loop
        # if not self.paused:
        self.all_sprites.update()

        # delays the screenshot taking to reduce file size
        if self.image_cooldown > 0:
            self.image_cooldown -= 1

    # draw the grid for the map
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

    def draw(self):
        # draw items in game loop
        self.screen.blit(self.background, (0, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        for tank in self.tanks:
            tank.display_health(tank.health_x_pos, TANK_HEALTH_Y)

        # flip display after drawing
        pygame.display.flip()

        # takes screenshots of the game to create gif
        if self.image_cooldown == 0:
            self.image_cooldown = IMAGE_COOLDOWN
            game_image = pygame.image.tostring(self.screen, "RGB", )
            formated_image = Image.frombytes("RGB", (WIDTH, HEIGHT), game_image)
            self.images.append(formated_image)

if __name__ == "__main__":
    game = Game()

    while True:
        try:
            game.new_instance()
            game.run()
        finally:
            game.images[0].save("Test.gif", save_all=True, append_images=game.images[1:], duration=100, loop=0)