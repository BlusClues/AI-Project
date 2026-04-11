import pygame

from Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.source_image = pygame.transform.rotozoom(pygame.image.load('Assets/BlueTank.png').convert_alpha(), -90, TANKSCALE)
        self.image = self.source_image.copy()

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

    def rotate_sprite(self, angle):
        rotation_angle = (round(angle / 90)) * 90
        self.image = pygame.transform.rotate(self.source_image, rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.x = self.x*TILESIZE
        self.rect.y = self.y*TILESIZE