# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame

# importing everything from constants.py
from constants import *

def main():
    print("Starting Asteroids!")
    print(f"Screen width:",SCREEN_WIDTH)
    print(f"Screen height:",SCREEN_HEIGHT)

# initialize pygame, define screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# infinite loop to keep the window open
    while True:
# checks if the user has clicked the 'X' button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        pygame.display.flip()

if __name__ == "__main__":
    main()