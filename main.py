import pygame
from pygame.locals import *
from classes import Player, Platform
 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
 
HEIGHT = 900
WIDTH = 800
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

player = Player(30, 30, 30, HEIGHT - 50)
floor = Platform(WIDTH, 50, WIDTH / 2, HEIGHT - 25)

allSprites = pygame.sprite.Group()
allSprites.add(player)
allSprites.add(floor)
platforms = pygame.sprite.Group()
platforms.add(floor)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    displaysurface.fill((0,0,0))

    player.move()

    for entity in allSprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)
