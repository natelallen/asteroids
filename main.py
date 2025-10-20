# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player

def main():
    print("Starting Asteroids!")
    print(f"Screen width:",SCREEN_WIDTH)
    print(f"Screen height:",SCREEN_HEIGHT)

# initialize pygame, define screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, PLAYER_RADIUS)
    dt = 0

# infinite loop to run the game window
    while True:
        dt = clock.tick(60) / 1000 # limit framerate to 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        player.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()