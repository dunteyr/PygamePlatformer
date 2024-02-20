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
score = 0
startDelay = 2000
scoreSpeed = 400
platsMoving = False

platMoveEvent = pygame.event.Event(2)
scoreEvent = pygame.event.Event(1)
clock = pygame.time.Clock()
font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
 
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

pygame.time.set_timer(scoreEvent, scoreSpeed)
pygame.time.set_timer(platMoveEvent, startDelay, 1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == scoreEvent.type:
            score += 1
        if event.type == platMoveEvent.type:
            platsMoving = True
    displaysurface.fill((0,0,0))

    if platsMoving:
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
        #stop the score
        pygame.time.set_timer(scoreEvent, 0)
        #stop the platforms
        platsMoving = False
        player.rect.bottom = HEIGHT - 10
        player.kill()

    #draw all sprites
    for entity in allSprites:
        displaysurface.blit(entity.surf, entity.rect)

    #draw score
    scoreText = font.render(f"Score: {score}", True, (255, 255, 255))
    displaysurface.blit(scoreText, (20, 20))

    pygame.display.update()
    clock.tick(FPS)