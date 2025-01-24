import random
import pygame, sys
from pygame.locals import *

from utils import getCurrentTime
from const import *
from block import *


class BlockGroup(object):
    def GenerateBlockGroupConfig(rowIdx, colIdx, shapeIdx=-1):
        if shapeIdx == -1:  # generate new block shape if shapeIdx is -1
            shapeIdx = random.randint(0, len(BLOCK_SHAPE) - 1)

        bType = random.randint(0, BlockType.BLOCKMAX - 1)
        configList = []
        rotIdx = 0
        for i in range(len(BLOCK_SHAPE[shapeIdx][rotIdx])):
            config = {
                'blockType': bType,
                'blockShape': shapeIdx,
                'blockRot': rotIdx,
                'blockGroupIdx': i,
                'rowIdx': rowIdx,
                'colIdx': colIdx,
            }
            configList.append(config)
        return configList

    def __init__(self, blockGroupType, width, height, blockConfigList, relPos):
        super().__init__()

        self.dropTime = getCurrentTime()
        self.blocks = []
        self.pressTime = {}  # store press time of each key
        self.dropInterval = 0
        self.blockGroupType = blockGroupType
        self.isEliminating = False
        self.eliminateTime = 0
        self.eliminateRow = 0
        for config in blockConfigList:
            blk = Block(config['blockType'], config['rowIdx'], config['colIdx'], config['blockShape'],
                        config['blockRot'], config['blockGroupIdx'], width,
                        height, relPos)
            self.blocks.append(blk)

    def setBaseIndexes(self, baseRow, baseCol):
        for blk in self.blocks:
            blk.setBaseIndex(baseRow, baseCol)

    def getBlockIndexes(self):
        return [block.getIndex() for block in self.blocks]

    def getNextBlockIndexes(self):
        return [block.getNextIndex() for block in self.blocks]

    def getBlocks(self):
        return self.blocks

    def clearBlocks(self):
        self.blocks = []

    def addBlocks(self, blk):
        self.blocks.append(blk)

    def checkAndSetPressTime(self, key):
        ret = False
        if getCurrentTime() - self.pressTime.get(key, 0) > 150:
            ret = True
            self.pressTime[key] = getCurrentTime()
        return ret

    def keyDownHandler(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and self.checkAndSetPressTime(K_LEFT):
            b = True
            for blk in self.blocks:
                if blk.isLeftBound():
                    b = False
                    break
            if b:
                for blk in self.blocks:
                    blk.doLeft()
        elif pressed[K_RIGHT] and self.checkAndSetPressTime(K_RIGHT):
            b = True
            for blk in self.blocks:
                if blk.isRightBound():
                    b = False
                    break
            if b:
                for blk in self.blocks:
                    blk.doRight()

        if pressed[K_DOWN]:
            self.dropInterval = 30
        else:
            self.dropInterval = 1000

        if pressed[K_UP] and self.checkAndSetPressTime(K_UP):
            for blk in self.blocks:
                blk.doRotate()

    def doEliminate(self, row):
        eliminateRow = {}
        for col in range(GAME_COL):
            idx = (row, col)
            eliminateRow[idx] = 1
        self.setEliminate(True)
        self.eliminateRow = row

        for blk in self.blocks:
            if eliminateRow.get(blk.getIndex()):
                blk.startBlink()

    def processEliminate(self):
        hash = {}  #
        allIndexes = self.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1

        for row in range(GAME_ROW - 1, -1, -1):
            full = True
            for col in range(GAME_COL):
                idx = (row, col)
                if not hash.get(idx):
                    full = False
                    break
            if full:
                self.doEliminate(row)
                return True

    def setEliminate(self, el):
        self.isEliminating = el
        self.eliminateTime = getCurrentTime()

    def IsEliminating(self):
        return self.isEliminating

    def update(self):
        oldTime = self.dropTime
        curTime = getCurrentTime()
        diffTime = curTime - oldTime
        if self.blockGroupType == BlockGroupType.DROP:
            if diffTime >= self.dropInterval:
                self.dropTime = curTime
                for b in self.blocks:
                    b.drop()
            self.keyDownHandler()
        for blk in self.blocks:
            blk.update()
        if self.IsEliminating():
            if getCurrentTime() - self.eliminateTime > 500:
                tmpBlocks = []
                for blk in self.blocks:
                    if blk.getIndex()[0] != self.eliminateRow:
                        if blk.getIndex()[0] < self.eliminateRow:
                            blk.drop()
                        tmpBlocks.append(blk)
                self.blocks = tmpBlocks
                self.setEliminate(False)

    def draw(self, surface):
        for b in self.blocks:
            b.draw(surface)
