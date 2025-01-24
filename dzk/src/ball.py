import pygame
from pygame.locals import *
from const import *
from utils import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, imgPath, x, y, dirX, dirY):
        super().__init__()
        self.posX = x
        self.posY = y
        self.dirX = dirX
        self.dirY = dirY
        self.speed = 0.5
        img = pygame.image.load(imgPath)
        img = pygame.transform.scale(img, (SPRITE_SIZE_W, SPRITE_SIZE_H))
        self.image = img
        self.rect = self.image.get_rect()
        self.preRotateTime = 0
        self.jntmSound = pygame.mixer.Sound(SoundRes.JNTM)
        self.ngmSound = pygame.mixer.Sound(SoundRes.NGM)

    def update(self):
        self.posX += self.dirX * self.speed
        self.posY += self.dirY * self.speed
        self.rect.x = self.posX
        self.rect.y = self.posY
        if getCurrentTime() - self.preRotateTime > 50:
            self.preRotateTime = getCurrentTime()
            self.image = pygame.transform.rotate(self.image, (getCurrentTime() % 4 - 2) * 90)

    def getRect(self):
        return self.rect

    def draw(self, surface):
        surface.blit(self.image, self.getRect())

    def changeDirection(self, rect):
        self.jntmSound.play()
        if abs(self.getRect().x - rect.x) <= abs(self.getRect().y - rect.y):
            self.dirY *= -1
        else:
            self.dirX *= -1

    def changeYDirection(self, rect):
        self.ngmSound.play()
        if abs(self.getRect().x - rect.x) <= abs(self.getRect().y - rect.y):
            self.dirY *= -1
        else:
            self.dirX *= 1
            if self.dirY > 0:
                self.dirY *= -1

    def setSpeed(self, speed):
        self.speed = speed
