import pygame
from sys import exit
import math
from Settings import *

# Adding pygame
pygame.init()

# Creating the window
# https://www.youtube.com/watch?v=OUOI6iCrmCk
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Game")
clock = pygame.time.Clock()

# Load Assets
background = pygame.transform.scale(pygame.image.load('Assets/background.png').convert(), (WIDTH, HEIGHT))
# tank = pygame.image.load('Assets/tank.png').convert()

# Defining the player for testing purposes
class PlayerTank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/Tank1.png').convert_alpha(), 0, 1.5)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)

player = PlayerTank()

# Game Loop
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Fill the background
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.pos)

    # Update the game
    pygame.display.update()
    clock.tick(FPS)

