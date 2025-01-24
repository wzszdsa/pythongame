import pygame
from pygame.locals import *
from const import *
from pather import Pather
from utils import *
import random

class Level(object):
    def __init__(self,level):
        self.map = []
        self.dynamicObjIndexes = {
            SpriteType.GOAL:[],
            SpriteType.BOX:[],
            SpriteType.PLAYER:[]
        }
        self.row = 1
        self.col = 1
        self.level = level
        self.pressTime = {}
        self.pather = Pather()
        self.loadLevel()
    
    def loadLevel(self):
        self.autoMoveIndex = 0
        self.lastAutoMoveTime = getCurrentTime()
        self.map = []
        goalIndexes = []
        boxIndexes = []
        playerIndex = []
        with open ('data/level/' + str(self.level) + '.x','r') as f:
            lines = f.readlines()
            r,c = lines[0].split(' ')
            self.row = int(r)
            self.col = int(c)
            r = 0
            for line in lines[1:]:
                mapRow = []
                for c in range(self.col):
                    if line[c] == SpriteType.BOX:
                        mapRow.append(SpriteType.FLOOR)
                        boxIndexes.append([r,c])
                    elif line[c] == SpriteType.PLAYER:
                        mapRow.append(SpriteType.FLOOR)
                        playerIndex.append([r, c])
                    elif line[c] == SpriteType.GOAL:
                        mapRow.append(SpriteType.FLOOR)
                        goalIndexes.append([r, c])
                    else:
                        mapRow.append(line[c])
                self.map.append(mapRow)
                r += 1
        self.dynamicObjIndexes = {
            SpriteType.GOAL:goalIndexes,
            SpriteType.BOX:boxIndexes,
            SpriteType.PLAYER:playerIndex
        }
        self.pather.startRecord(self.level)

    def getMap(self):
        return self.map
    
    def getDynamicObjIndexes(self,sType):
        return self.dynamicObjIndexes[sType]

    def checkAndSetPressTime(self,key):
        ret = False
        if getCurrentTime() - self.pressTime.get(key,0) > 150:
            ret = True
            self.pressTime[key] = getCurrentTime()
        return ret

    def keyDownHandler(self):
        pressed = pygame.key.get_pressed()
        for i,key in enumerate(DIR_KEY):
            if pressed[key] and self.checkAndSetPressTime(key):
               self.move(i)
    def autoMove(self):
        if getCurrentTime() - self.lastAutoMoveTime > 500:
            self.lastAutoMoveTime = getCurrentTime()
            if self.autoMoveIndex < len(self.pather.getRecord()):
                self.move(self.pather.getRecord()[self.autoMoveIndex])
                self.autoMoveIndex += 1
            else:
                self.move(random.randint(0,3))

    def move(self,i):
        playerIndex = self.getDynamicObjIndexes(SpriteType.PLAYER)[0]
        r,c = playerIndex[0],playerIndex[1]
        nr = r + DIR[i][0]
        nc = c + DIR[i][1]
        if self.isFloor(nr,nc):
            self.setPlayerIndex(nr,nc)
            self.pather.addRecord(i)
        elif self.isBox(nr, nc):
            if self.canPush(nr, nc, i):
                self.setPlayerIndex(nr, nc)
                self.pushBox(nr, nc, i)
                self.pather.addRecord(i)


    def setPlayerIndex(self,r,c):   
        playerPos = self.getDynamicObjIndexes(SpriteType.PLAYER)
        playerPos[0] = [r, c]

    def isFloor(self, r, c):
        if r < 0 or c < 0:
            return False
        if r >= self.row or c >= self.col:
            return False
        if self.map[r][c] == SpriteType.WALL:
            return False
        for box in self.getDynamicObjIndexes(SpriteType.BOX):
            if box[0] == r and box[1] == c:
                return False
        return True
    
    def isBox(self,r,c):
        for box in self.getDynamicObjIndexes(SpriteType.BOX):
            if box[0] == r and box[1] == c:
                return True
        return False
    
    def canPush(self,r,c,d):
        nr = r + DIR[d][0]
        nc = c + DIR[d][1]
        return self.isFloor(nr, nc)
    
    def pushBox(self,r,c,d):
        for box in self.getDynamicObjIndexes(SpriteType.BOX):
            if box[0] == r and box[1] == c:
               box[0] += DIR[d][0]
               box[1] += DIR[d][1]
               self.setPlayerIndex(r, c)
               return
    
    def checkFinish(self):
        for box in self.getDynamicObjIndexes(SpriteType.BOX):
            find = False
            for goal in self.getDynamicObjIndexes(SpriteType.GOAL):
                if box[0] == goal[0] and box[1] == goal[1]:
                    find = True
                    break
            if not find:
                return False
        return True
    
    def checkLevel(self):
        if self.checkFinish():
            if self.level < 6:
                self.pather.dumpRecord()
                self.level += 1
                self.loadLevel()
            return True
        return False