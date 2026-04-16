import pygame

from Settings import *
from Tank import Tank

class Player(Tank):
    def __init__(self, game, x, y, id):
        super().__init__(game, x, y, id, BLUE_TANK_SPRITE_PATH, BLUE, BLUE_BULLET_SPRITE_PATH)

    def events(self):
        # handle events in game loop
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.game.quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                    self.current_angle = 0
                    self.rotate_sprite(self.current_angle)
                    self.move(dx=-1)
                if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                    self.current_angle = 180
                    self.rotate_sprite(self.current_angle)
                    self.move(dx=1)
                if e.key == pygame.K_DOWN or e.key == pygame.K_s:
                    self.current_angle = 90
                    self.rotate_sprite(self.current_angle)
                    self.move(dy=1)
                if e.key == pygame.K_UP or e.key == pygame.K_w:
                    self.current_angle = -90
                    self.rotate_sprite(self.current_angle)
                    self.move(dy=-1)

        # detects button for shooting
        if pygame.mouse.get_pressed() == (1, 0, 0) or pygame.key.get_pressed()[pygame.K_SPACE]:
            self.shoot()

    def update(self):
        super().update()
        self.events()