import image
from utils import *
import data_object


class ObjectBase(image.Image):
    def __init__(self, id, pos):
        self.id = id
        self.hp = self.getData()['HP']
        self.attack = self.getData()['ATT']
        self.preIndexTime = 0
        self.prePositionTime = 0
        self.preSummonTime = 0
        super(ObjectBase, self).__init__(self.getData()['PATH'], 0, pos, self.getData()['SIZE'],
                                         self.getData()['IMAGE_INDEX_MAX'])

    def getData(self):
        return data_object.data[self.id]

    def getPositionCD(self):
        return self.getData()['POSITION_CD']

    def getImageIndexCD(self):
        return self.getData()['IMAGE_INDEX_CD']

    def getSpeed(self):
        return self.getData()['SPEED']

    def getSummonCD(self):
        return self.getData()['SUMMON_CD']

    def getPrice(self):
        return self.getData()['PRICE']

    def update(self):
        self.checkImageIndex()
        self.checkPosition()
        self.checkSummon()

    def checkImageIndex(self):
        if getCurrentTime() - self.preIndexTime <= self.getImageIndexCD():
            return
        self.preIndexTime = getCurrentTime()
        idx = self.pathIndex + 1
        if idx >= self.pathIndexCount:
            idx = 0
        self.updateIndex(idx)

    def checkPosition(self):
        if getCurrentTime() - self.prePositionTime <= self.getPositionCD():
            return
        self.prePositionTime = getCurrentTime()
        speed = self.getSpeed()

        self.pos = (self.pos[0] + speed[0], self.pos[1] + speed[1])
        return True

    def checkSummon(self):
        if getCurrentTime() - self.preSummonTime <= self.getSummonCD():
            return
        self.preSummonTime = getCurrentTime()
        self.preSummon()

    def preSummon(self):
        pass

    def canLoot(self):
        return self.getData()['CAN_LOOT']

    def isCollide(self, other):
        return self.getRect().colliderect(other.getRect())
