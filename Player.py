import pygame

from Settings import *
from Bullet import Bullet

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
        self.shoot_cooldown = 0
        self.angle = 0

    # detect collision with walls
    def colliding_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if (self.x + dx) == wall.x and (self.y + dy) == wall.y:
                return True
        return False

    # calculate movement for tanks
    def move(self, dx=0, dy=0):
        if not self.colliding_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    # rotate the sprite depending on movement direction
    def rotate_sprite(self, angle):
        self.image = pygame.transform.rotate(self.source_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    # Shoots bullet
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_x, spawn_y = self.rect.center
            self.bullet = Bullet(self.game, spawn_x, spawn_y, self.game.current_angle, self.groups)

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        # adds cooldown to shooting to stop rapid fire
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1