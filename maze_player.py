""" Maze player """
import sys
import pygame
import maze_gen


def main():
    pygame.init()
    pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Maze Player')

    clock = pygame.time.Clock()

    maze = maze_gen.create_maze(5, 5)
    print(maze)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
