from game import *
import pygame
from pygame.locals import *
from const import *

if __name__ == '__main__':
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE))
    game = Game(DISPLAYSURF)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        game.update()
        DISPLAYSURF.fill((0, 0, 0))
        game.draw()
        pygame.display.update()
