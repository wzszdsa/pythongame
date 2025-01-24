import pygame
from pygame.locals import *
from const import *
from sprite import *
from level import *

class Game(object):
    def __init__(self,surface,relativePos,controlType):
        self.surface = surface
        self.relativePos = relativePos
        self.level = Level(6)
        self.controlType = controlType
        self.loadLevel()
    
    @property
    def row(self):
        return self.level.row
    
    @property
    def col(self):
        return self.level.col
    
    @property
    def map(self):
        return self.level.getMap()

   
    def loadLevel(self):
        self.level.loadLevel()
        self.loadMapSprites()
        self.loadDynamicSprites()
            
    def loadMapSprites(self):
        self.mapSprites = []
        for i in range(self.row):
            mapSpriteRow = []
            for j in range(self.col):
                sType = self.map[i][j]
                res = SPRITE_RES[sType]
                spr = Sprite(res,i,j,self.relativePos)
                mapSpriteRow.append(spr)
            self.mapSprites.append(mapSpriteRow)
    
    def loadSprites(self,sType,posList):
        spriteList = []
        for pos in posList:
            res = SPRITE_RES[sType]
            spr = Sprite(res, pos[0], pos[1], self.relativePos)
            spriteList.append(spr)
        return spriteList

    def loadDynamicSprites(self):
        self.goalSprites = self.loadSprites(SpriteType.GOAL, self.level.getDynamicObjIndexes(SpriteType.GOAL))
        self.playerSprite = self.loadSprites(SpriteType.PLAYER, self.level.getDynamicObjIndexes(SpriteType.PLAYER))[0]
        self.boxSprites = self.loadSprites(SpriteType.BOX, self.level.getDynamicObjIndexes(SpriteType.BOX))

    def updateDynamicSprites(self):
        goalIndexes = self.level.getDynamicObjIndexes(SpriteType.GOAL)
        boxIndexes = self.level.getDynamicObjIndexes(SpriteType.BOX)
        playerIndex = self.level.getDynamicObjIndexes(SpriteType.PLAYER) [0]
        for i,goal in enumerate(self.goalSprites):
            goal.updateIdx(*goalIndexes[i])
        for i,box in enumerate(self.boxSprites):
            box.updateIdx(*boxIndexes[i])
        self.playerSprite.updateIdx(*playerIndex)

    def update(self):
        self.updateDynamicSprites()
        if self.controlType == ControlType.REN:
            self.level.keyDownHandler()
            pressed = pygame.key.get_pressed()
            if pressed[K_r]:
                self.loadLevel()
        else:
            self.level.autoMove()
        if self.level.checkLevel():
                self.loadLevel()
                
        

    def drawDynamicSprites(self):
        for goal in self.goalSprites:
            goal.draw(self.surface)
        for box in self.boxSprites:
            box.draw(self.surface)
        self.playerSprite.draw(self.surface)

    def draw(self):
        if self.level.level <= 6:
            self.drawMap()
            self.drawDynamicSprites()
        else:
            self.surface.fill((0,0,0))
            image = pygame.image.load("res/win.png")
            self.surface.blit(image,image.get_rect())
    def drawMap(self):
        for i in range(self.row):
            for j in range(self.col):
                self.mapSprites[i][j].draw(self.surface)

    