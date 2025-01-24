import pygame


class Image(pygame.sprite.Sprite):
    def __init__(self, pathFmt, pathIndex, pos, size, pathIndexCount):
        super().__init__()
        self.pathFmt = pathFmt
        self.pathIndex = pathIndex
        self.pathIndexCount = pathIndexCount
        self.size = size
        self.pos = list(pos)
        self.updateImage()

    def updateImage(self):
        path = self.pathFmt
        if self.pathIndexCount != 0:
            path = path % self.pathIndex
        self.image = pygame.image.load(path)
        if self.size:
            self.image = pygame.transform.scale(self.image, self.size)

    def updateSize(self, size):
        self.size = size
        self.updateImage()

    def updateIndex(self, pathIndex):
        self.pathIndex = pathIndex
        self.updateImage()

    def getRect(self):
        rect = self.image.get_rect()
        rect.x, rect.y = self.pos
        return rect

    def doLeft(self):
        self.pos[0] -= 0.1

    def draw(self, ds):
        ds.blit(self.image, self.getRect())
