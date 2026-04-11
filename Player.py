import pygame

from Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def colliding_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if (self.x + dx) == wall.x and (self.y + dy) == wall.y:
                return True

        return False

    def move(self, dx=0, dy=0):
        if not self.colliding_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def update(self):
        self.rect.x = self.x*TILESIZE
        self.rect.y = self.y*TILESIZE