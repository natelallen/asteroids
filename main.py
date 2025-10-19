# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame

# importing everything from constraints.py
from constants import *

def main():
    print("Starting Asteroids!")
    print(f"Screen width:",SCREEN_WIDTH)
    print(f"Screen height:",SCREEN_HEIGHT)


if __name__ == "__main__":
    main()
    # initialize pygame, define screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        # check if user has closed window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.Surface.fill(screen, ( 0, 0, 0))
        pygame.display.flip()