""" Maze player """
import sys
import pygame


def main():
    pygame.init()
    pygame.display.set_mode((320, 240))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        pygame.display.flip()
        pygame.time.delay(100)
    pass


if __name__ == "__main__":
    main()