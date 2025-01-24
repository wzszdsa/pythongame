import pygame, sys
from pygame.locals import *
from const import *
from block import *
from blockGroup import *


class Game(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.font = pygame.font.Font(None, 60)
        self.score = 0
        self.surface = surface
        self.gameOverImage = pygame.image.load("../img/lose.jpg")
        self.isGameOver = False
        self.fixedBlockGroup = BlockGroup(BlockGroupType.FIXED, BLOCK_SIZE_W, BLOCK_SIZE_H, [], self.getRelPos())
        self.dropBlockGroup = None
        self.nextBlockGroup = None
        self.generateNextBlockGroup()

    def generateDropBlockGroup(self):
        self.dropBlockGroup = self.nextBlockGroup
        self.dropBlockGroup.setBaseIndexes(0, GAME_COL / 2 - 1)
        self.generateNextBlockGroup()

    def generateNextBlockGroup(self):
        conf = BlockGroup.GenerateBlockGroupConfig(0, GAME_COL + 3)
        self.nextBlockGroup = BlockGroup(BlockGroupType.DROP, BLOCK_SIZE_W, BLOCK_SIZE_H, conf, self.getRelPos())

    def update(self):
        if self.isGameOver:
            return
        self.fixedBlockGroup.update()
        if self.fixedBlockGroup.isEliminating:
            return
        if self.dropBlockGroup:
            self.dropBlockGroup.update()
        else:
            self.generateDropBlockGroup()
        if self.willCollide():
            blocks = self.dropBlockGroup.getBlocks()
            for b in blocks:
                self.fixedBlockGroup.addBlocks(b)
            self.dropBlockGroup.clearBlocks()
            self.dropBlockGroup = None
            if self.fixedBlockGroup.processEliminate():
                self.score += 1

        self.checkGameOver()

    def checkGameOver(self):
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            if idx[0] < 2:
                self.isGameOver = True

    def draw(self):
        self.fixedBlockGroup.draw(self.surface)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.surface)
        self.nextBlockGroup.draw(self.surface)

        if self.isGameOver:
            rect = self.gameOverImage.get_rect()
            rect.centerx = GAME_WIDTH_SIZE / 2
            rect.centery = GAME_HEIGHT_SIZE / 2
            self.surface.blit(self.gameOverImage, rect)

        textImage = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.surface.blit(textImage, (10, 20))

    def getRelPos(self):
        return (240, 50)

    def willCollide(self):
        hash = {}
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1
        dropIndexes = self.dropBlockGroup.getNextBlockIndexes()

        for dropIndex in dropIndexes:
            if hash.get(dropIndex):
                return True
            if dropIndex[0] >= GAME_ROW:
                return True
        return False
