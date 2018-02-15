""" Maze player """
import sys
import pygame


def main():
    pygame.init()
    pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Maze Player')

    target_fps = 30.
    target_frame_duration = 1000. / target_fps

    last_ticks = 0

    clock = pygame.time.Clock()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()
        current_ticks = pygame.time.get_ticks()
        elapsed_duration = current_ticks - last_ticks

        if elapsed_duration < target_frame_duration:
            pygame.time.delay(int(target_frame_duration - elapsed_duration))

        last_ticks = pygame.time.get_ticks()
        clock.tick()
        # print(clock.get_fps())
    pass


if __name__ == "__main__":
    main()
