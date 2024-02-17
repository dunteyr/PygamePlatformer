import pygame
from pygame.locals import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()

        self.collisionGroups = []

        self.acceleration = 0.5
        self.friction = -0.12
        self.jumpAmt = -15

        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

        self.width = width
        self.height = height
        self.surf = pygame.Surface((width, height))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()

    def move(self):
        self.acc = vec(0, 0.5)

        collisions = self.getCollisions()

        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[K_a]:
            self.acc.x = -self.acceleration
        elif pressedKeys[K_d]:
            self.acc.x = self.acceleration

        if pressedKeys[K_SPACE]:
            self.jump()

        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #this is a hacky way to handle floor collision for now
        if collisions:
            self.pos.y = collisions[0].rect.top

            #without this if jumping velocity will be reset
            if self.vel.y > 0:
                self.vel.y = 0

        self.rect.midbottom = self.pos

    def update(self):
        pass

    def addCollisionGroup(self, collisionGroup):
        self.collisionGroups.append(collisionGroup)

    def getCollisions(self):
        collisions = []
        #get a list of collisions from every group that player can collide with
        for group in self.collisionGroups:
            groupCollisions = pygame.sprite.spritecollide(self, group, False)
            collisions += groupCollisions

        return collisions

    def jump(self):
        collisions = self.getCollisions()
        if collisions:
            self.vel.y = self.jumpAmt

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.width = width
        self.height = height
        self.surf = pygame.Surface((width, height))
        self.surf.fill((81, 95, 201))
        self.rect = self.surf.get_rect(center = (x, y))