import pygame

from Settings import *
from Bullet import Bullet

class Tank(pygame.sprite.Sprite):
    def __init__(self, game, x, y, id, image_path, text_colour, bullet_colour):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.source_image = pygame.transform.rotozoom(pygame.image.load(image_path).convert_alpha(), -90, TANKSCALE)
        self.image = self.source_image.copy()
        self.id = id
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.shoot_cooldown = 0
        self.angle = 0
        self.health = TANK_HEALTH
        self.heart = pygame.transform.rotozoom(pygame.image.load('Assets/Heart.png').convert_alpha(), 0, HEART_SCALE)
        self.empty_heart = pygame.transform.rotozoom(pygame.image.load('Assets/HeartEmpty.png').convert_alpha(), 0, HEART_SCALE)
        self.my_font = pygame.font.SysFont("Comic Sans", 36)
        self.text_surface = self.my_font.render(TANK_COLOURS[self.id], True, text_colour)
        self.bullet_colour = bullet_colour

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
            self.bullet = Bullet(self.game, spawn_x, spawn_y, self.current_angle, (self.groups, self.game.bullets), self.id, self.bullet_colour)

    def was_shot(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            self.game.paused = True

    # to dynamically display the current health
    def display_health(self, x, y):
        # tank colour name display
        self.game.screen.blit(self.text_surface, (x + (TILESIZE / 4), y - TILESIZE - (TILESIZE / 2)))

        # Changing the hearts depending on health
        for i in range(TANK_HEALTH):
            heart_x = x + i * TILESIZE
            if i < self.health:
                self.game.screen.blit(self.heart, (heart_x - 4, y - 4))
            else:
                self.game.screen.blit(self.empty_heart, (heart_x - 4, y - 4))

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        # adds cooldown to shooting to stop rapid fire
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # stops ability to shot yourself
        for bullet in self.game.bullets:
            if pygame.sprite.spritecollide(self, self.game.bullets, False):
                if bullet.owner != self.id:
                    self.was_shot()
                    bullet.kill()