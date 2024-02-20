import pygame
from pygame.locals import *
import random
from classes import Player, Platform
 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
 
HEIGHT = 900
WIDTH = 800
FPS = 60
screenVel = 1
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

player = Player(30, 30, WIDTH // 2, HEIGHT - 50)
floor = Platform(WIDTH, 50, WIDTH / 2, HEIGHT - 25)

allSprites = pygame.sprite.Group()
allSprites.add(player)
allSprites.add(floor)
platforms = pygame.sprite.Group()
platforms.add(floor)
respawnables = pygame.sprite.Group()

for i in range(10):
    height = HEIGHT / 10
    odd = True
    if i % 2 == 0:
        odd = False
    
    platform = Platform(50, 25, 0, height * i)
    platform.rect.centerx = platform.getRandX(odd, WIDTH)
    platforms.add(platform)
    allSprites.add(platform)
    respawnables.add(platform)

player.addCollisionGroup(platforms)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        # if event.type == KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.jump()

    displaysurface.fill((0,0,0))

    #moving and respawning platforms
    for i in range(len(platforms)):
        sprites = platforms.sprites()
        odd = True
        if i % 2 == 0:
            odd = False
        sprites[i].rect = sprites[i].rect.move(0, screenVel)
        #if sprites[i] is part of respawnables and off screen respawn it
        if respawnables in sprites[i].groups() and sprites[i].rect.top >= HEIGHT:
            newRect = sprites[i].surf.get_rect(center = (sprites[i].getRandX(odd, WIDTH), 0))
            sprites[i].rect = newRect
            
    player.move()

    #handle player death
    if player.rect.bottom >= HEIGHT:
        player.rect.bottom = HEIGHT - 10
        player.kill()

    for entity in allSprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)