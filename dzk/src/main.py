import pygame, sys
from game import *
from pygame.locals import *
from const import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode(GAME_SIZE)
game = Game(DISPLAYSURF)
if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if pygame.event == QUIT:
                pygame.quit()
                sys.exit()
        game.update()
        DISPLAYSURF.fill((255, 255, 255))
        game.draw()
        pygame.display.update()
