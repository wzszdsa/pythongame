import pygame 
from pygame.locals import *
import sys
from const import *
from game import *
pygame.init()
DISPLAYSURF = pygame.display.set_mode((GAME_WIDTH_SIZE,GAME_HEIGHT_SIZE))

gameRen = Game(DISPLAYSURF,(100,20),ControlType.REN)
gameJi = Game(DISPLAYSURF,(100,600),ControlType.JI)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    gameRen.update()
    gameJi.update()
    DISPLAYSURF.fill((0,0,0))
    gameRen.draw()
    gameJi.draw()
    if gameJi.level.level > gameRen.level.level:
        DISPLAYSURF.fill((0,0,0))
        image = pygame.image.load('res/lose.png')
        DISPLAYSURF.blit(image, image.get_rect())
    pygame.display.update()