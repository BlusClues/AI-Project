import pygame
import sys

from os import path

from Obstacles import Wall
from Settings import *
from Player import Player
from TileMap import Map

# Defining Variables
filename = 'TextMap.txt'

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # set the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        # game control
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 10)

        self.load()

    def load(self):
        game_dir = path.dirname(__file__)
        self.map = Map(path.join(game_dir, filename))

    def new_instance(self):
        # create a new instance of the game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        # create sprites
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '*':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)

        # self.player = Player(self, 0, 0)
        # for x in range(5, 10):
        #     Wall(self, x, 5)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update items in the game loop
        self.all_sprites.update()

    def events(self):
        # handle events in game loop
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.player.move(dx=-1)
                if e.key == pygame.K_RIGHT:
                    self.player.move(dx=1)
                if e.key == pygame.K_DOWN:
                    self.player.move(dy=1)
                if e.key == pygame.K_UP:
                    self.player.move(dy=-1)


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

    def draw(self):
        # draw items in game loop
        self.screen.fill(TAN)
        self.draw_grid()
        self.all_sprites.draw(self.screen)

        # flip display after drawing
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()

    while True:
        game.new_instance()
        game.run()