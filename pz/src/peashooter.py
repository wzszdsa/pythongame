import objectbase
import peabullet
from utils import *


class PeaShooter(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.hasShoot = False
        self.hasBullet = False

    def hasSummon(self):
        return self.hasBullet

    def preSummon(self):
        self.hasShoot = True
        self.pathIndex = 0

    def doSummon(self):
        if self.hasBullet:
            self.hasBullet = False
            return peabullet.PeaBullet(0, (self.pos[0] + 100, self.pos[1] + 40))

    def checkImageIndex(self):
        if getCurrentTime() - self.preIndexTime <= self.getImageIndexCD():
            return
        self.preIndexTime = getCurrentTime()

        idx = self.pathIndex + 1
        if idx == 8 and self.hasShoot:
            self.hasBullet = True
        if idx >= self.pathIndexCount:
            idx = 9
        self.updateIndex(idx)