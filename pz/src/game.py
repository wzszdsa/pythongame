import random

import pygame.mouse

import data_object
from asyncServer import *
from image import *
from peashooter import *
from sunflower import *
from zombiebase import *
from share.const import *


class Game(object):
    def __init__(self, ds):
        pygame.mixer.init()
        self.ds = ds
        self.back = Image(PATH_BACK, 0, (0, 0), GAME_SIZE, 0)
        self.plants = []
        self.summons = []
        self.hasPlant = []
        self.gold = 100
        self.goldFont = pygame.font.Font(None, 60)
        self.zombie = 0
        self.zombieFont = pygame.font.Font(None, 60)
        for i in range(GRID_SIZE[0]):
            col = []
            for j in range(GRID_SIZE[1]):
                col.append(0)
            self.hasPlant.append(col)
        self.zombieGenerateTime = 0
        self.zombies = []
        self.isGameOver = False
        self.loseImg = Image(PATH_LOSE, 0, (0, 0), GAME_SIZE, 0)
        self.client = AsyncServer(self, SERVER_IP, SERVER_PORT)

    def renderFont(self):
        textImage = self.goldFont.render("Gold: " + str(self.gold), True, (0, 0, 0))
        self.ds.blit(textImage, (13, 23))
        textImage = self.goldFont.render("Gold: " + str(self.gold), True, (255, 255, 255))
        self.ds.blit(textImage, (10, 20))
        textImage = self.zombieFont.render("Score: " + str(self.zombie), True, (0, 0, 0))
        self.ds.blit(textImage, (13, 83))
        textImage = self.zombieFont.render("Score: " + str(self.zombie), True, (255, 255, 255))
        self.ds.blit(textImage, (10, 80))

    def draw(self):
        if self.isGameOver:
            self.loseImg.draw(self.ds)
            return
        self.back.draw(self.ds)
        for plant in self.plants:
            plant.draw(self.ds)
        for summon in self.summons:
            summon.draw(self.ds)
        for zombie in self.zombies:
            zombie.draw(self.ds)
        self.renderFont()

    def update(self):
        self.back.update()
        for plant in self.plants:
            plant.update()
            if plant.hasSummon():
                summ = plant.doSummon()
                self.summons.append(summ)
        for summon in self.summons:
            summon.update()
        for zombie in self.zombies:
            if zombie.getRect().x < 100:
                self.isGameOver = True
            zombie.update()

        if getCurrentTime() - self.zombieGenerateTime > ZOMBIE_BORN_CD:
            self.zombieGenerateTime = getCurrentTime()
            self.addZombie(ZOMBIE_BORN_X, random.randint(0, GRID_COUNT[1] - 1))
        self.checkZombieVSPlant()
        self.checkSummonVSZombie()

        for summon in self.summons:
            if summon.getRect().x > GAME_SIZE[0] or summon.getRect().y > GAME_SIZE[1]:
                self.summons.remove(summon)
                break

    def getIndexByPos(self, pos):
        x = (pos[0] - LEFT_TOP[0]) // GRID_SIZE[0]
        y = (pos[1] - LEFT_TOP[1]) // GRID_SIZE[1]
        return x, y

    def addSunFlower(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        sf = SunFlower(SUNFLOWER_ID, pos)
        self.plants.append(sf)

    def addPeaShooter(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        ps = PeaShooter(PEASHOOTER_ID, pos)
        self.plants.append(ps)

    def addZombie(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        zb = ZombieBase(ZOMBIE_ID, pos)
        self.zombies.append(zb)

    def checkLoot(self, mousePos):
        for summon in self.summons:
            if not summon.canLoot():
                continue
            rect = summon.getRect()
            if rect.collidepoint(mousePos):
                self.summons.remove(summon)
                self.gold += summon.getPrice()
                return True
        return False

    def addPlant(self, mousePos, objId):
        x, y = mousePos
        if x < 0 or x >= GRID_COUNT[0]:
            return
        if y < 0 or y >= GRID_COUNT[1]:
            return
        if self.gold < data_object.data[objId]['PRICE']:
            return
        if self.hasPlant[x][y] == 1:
            return
        self.hasPlant[x][y] = 1
        self.gold -= data_object.data[objId]['PRICE']
        if objId == SUNFLOWER_ID:
            self.addSunFlower(x, y)
        elif objId == PEASHOOTER_ID:
            self.addPeaShooter(x, y)

    def mouseClickHandler(self, btn):

        if self.isGameOver:
            return
        mousePos = pygame.mouse.get_pos()
        if self.checkLoot(mousePos):
            return
        plantIdx = -1
        if btn == 1:
            plantIdx = SUNFLOWER_ID
        elif btn == 3:
            plantIdx = PEASHOOTER_ID
        if plantIdx != -1:
            asyncio.run(
                self.client.c2s({'type': C2S_ADD_PLANT, 'pos': self.getIndexByPos(mousePos), 'plant_idx': plantIdx}))

    def fight(self, a, b):
        while True:
            a.hp -= b.attack
            b.hp -= a.attack
            if b.hp <= 0:
                return True
            if a.hp <= 0:
                return False

    def checkSummonVSZombie(self):
        for summon in self.summons:
            for zombie in self.zombies:
                if summon.isCollide(zombie):
                    self.fight(summon, zombie)
                    if zombie.hp <= 0:
                        self.zombies.remove(zombie)
                        self.zombie += 1
                    if summon.hp <= 0:
                        self.summons.remove(summon)

    def checkZombieVSPlant(self):
        for zombie in self.zombies:
            for plant in self.plants:
                if zombie.isCollide(plant):
                    self.fight(zombie, plant)
                    if plant.hp <= 0:
                        self.plants.remove(plant)
                        break
