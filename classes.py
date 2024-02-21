import pygame
from pygame.locals import *
import random

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()

        self.isControllable = True
        self.isDead = False
        self.collisionGroups = []

        self.maxFall = 13.0
        self.acceleration = 0.5
        self.friction = -0.12
        self.jumpAmt = -15
        self.landed = False
        self.jumping = False

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

        #ignore collisions if dead
        if not self.isDead:
            collisions = self.getCollisions()
        else:
            collisions = None

        if self.isControllable:
            pressedKeys = pygame.key.get_pressed()

            if pressedKeys[K_a]:
                self.acc.x = -self.acceleration
            elif pressedKeys[K_d]:
                self.acc.x = self.acceleration

            if pressedKeys[K_SPACE]:
                self.jump()
            if not pressedKeys[K_SPACE]:
                self.cancelJump()

        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        #dont let player go too fast or he'll go through platforms
        if self.vel.y >= self.maxFall:
            self.vel.y = self.maxFall
        self.pos += self.vel + 0.5 * self.acc

        #this is a hacky way to handle floor collision for now
        if collisions:
            #without this if jumping velocity will be reset
            if self.vel.y > 0:
                if self.pos.y < collisions[0].rect.bottom:
                    self.pos.y = collisions[0].rect.top
                    self.vel.y = 2.3
                    self.landed = True
                    self.jumping = False
        else:
            self.landed = False
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
        if self.landed:
            self.vel.y = self.jumpAmt
            self.landed = False
            self.jumping = True

    def cancelJump(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
                self.jumping = False

    def kill(self):

        if not self.isDead:
            self.friction = 0
            deathVel = 10
            xVel = random.randint(-deathVel // 2, deathVel // 2)
            yVel = -deathVel * 2
            self.surf.fill((255, 0, 0))
            self.vel = vec(xVel, yVel)
            self.isDead = True
            self.isControllable = False
        else:
            super().kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.width = width
        self.height = height
        self.surf = pygame.Surface((width, height))
        self.surf.fill((81, 95, 201))
        self.rect = self.surf.get_rect(center = (x, y))

    #takes screen width and whether plat is odd in its group
    def getRandX(self, isOdd, width):
        return random.randint(isOdd * (width // 2), (width // 2) * (isOdd + 1))