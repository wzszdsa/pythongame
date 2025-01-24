import pygame
from pygame.locals import *
from const import *
from player import *
from ball import *
from level import *
from block import *


class Game(object):
    def __init__(self, surface):
        pygame.mixer.init()
        self.surface = surface
        self.Load(1)

    def Load(self, lv):
        self.level = Level(lv)
        self.isGameOver = False
        self.balls = []
        self.loadPlayer()
        self.loadOneBall(self.player.getRect().x, self.player.getRect().y - SPRITE_SIZE_H - 5, 1, -1)
        self.loadBlockImages()

    def loadPlayer(self):
        self.player = Player(
            PLAYER_RES,
            (GAME_SIZE[0] - PLAYER_SIZE_W) / 2, GAME_SIZE[1] - PLAYER_SIZE_H,
            SPRITE_SIZE_W, GAME_SIZE[0] - PLAYER_SIZE_W - SPRITE_SIZE_W)

    def loadOneBall(self, x, y, dirX, dirY):
        ball = Ball(BALL_RES, x, y, dirX, dirY)
        self.balls.append(ball)

    def loadBlockImages(self):
        self.blocks = []
        for block in self.level.getBlocks():
            sp = Block(block[2], block[0], block[1], (0, 0))
            self.blocks.append(sp)

    def update(self):
        if self.isGameOver:
            return
        self.player.update()
        [ball.update() for ball in self.balls]
        [block.update() for block in self.blocks]
        self.checkBallBlockCollide()
        self.checkBallPlayerCollide()
        if self.isGameWin():
            self.Load(self.level.level + 1)
        flag = True
        while flag:
            flag = False
            for ball in self.balls:
                if ball.getRect().y > GAME_SIZE[1]:
                    self.balls.remove(ball)
                    flag = True
                    break
        if len(self.balls) == 0:
            self.isGameOver = True

    def draw(self):
        if self.isGameOver:
            img = pygame.image.load(GAME_OVER_RES)
            self.surface.blit(img, img.get_rect())
            return
        self.player.draw(self.surface)
        [block.draw(self.surface) for block in self.blocks]
        [ball.draw(self.surface) for ball in self.balls]

    def checkBallBlockCollide(self):
        for ball in self.balls:
            for block in self.blocks:
                if ball.getRect().colliderect(block.getRect()):
                    ball.changeDirection(block.getRect())
                    self.processBlock(ball, block)
                    break

    def checkBallPlayerCollide(self):
        for ball in self.balls:
            if ball.getRect().colliderect(self.player.getRect()):
                ball.changeYDirection(self.player.getRect())
                break

    def processBlock(self, ball, block):
        if block.getBlockType() == BlockType.NORMAL:
            self.blocks.remove(block)
        if block.getBlockType() == BlockType.COPY:
            self.blocks.remove(block)
            self.copyBalls()
        if block.getBlockType() == BlockType.SPEED_UP:
            self.blocks.remove(block)
            ball.setSpeed(0.8)
        if block.getBlockType() == BlockType.SPEED_DOWN:
            self.blocks.remove(block)
            ball.setSpeed(0.3)

    def copyBalls(self):
        balls = [ball for ball in self.balls]
        for ball in balls:
            self.loadOneBall(ball.getRect().x, ball.getRect().y, 1, -1)

    def isGameWin(self):
        for block in self.blocks:
            if block.getBlockType() != BlockType.WALL:
                return False
        return True
