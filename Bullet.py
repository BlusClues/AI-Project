import pygame
import math

from Settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, angle, groups):
        super().__init__(groups)
        self.game = game
        self.source_image = pygame.image.load('Assets/BlueBullet.png').convert_alpha()
        self.source_image = pygame.transform.rotozoom(self.source_image, 90, BULLET_SCALE)
        self.image = self.source_image.copy()
        self.rect = self.source_image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.bullet_life = BULLET_LIFETIME

    # calculate the bullets movement
    def bullet_movement(self):
        self.x += -self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # kill bullet if it collides with a wall
        if pygame.sprite.spritecollide(self, self.game.walls, False):
            self.kill()

    # rotate the bullet sprite to match direction shot
    def rotate_bullet(self):
        self.image = pygame.transform.rotate(self.source_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rotate_bullet()
        self.bullet_movement()

        # kill bullet after time limit to prevent lag
        self.bullet_life -= self.game.dt
        if self.bullet_life <= 0:
            self.kill()
