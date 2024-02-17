import pygame
from pygame.locals import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()

        self.acceleration = 0.5
        self.friction = -0.12

        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

        self.width = width
        self.height = height
        self.surf = pygame.Surface((width, height))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()

    def move(self):
        self.acc = vec(0, 0)

        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[K_a]:
            self.acc.x = -self.acceleration
        elif pressedKeys[K_d]:
            self.acc.x = self.acceleration

        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

    def update(self):
        pass

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.width = width
        self.height = height
        self.surf = pygame.Surface((width, height))
        self.surf.fill((81, 95, 201))
        self.rect = self.surf.get_rect(center = (x, y))