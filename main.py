# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame, sys
from constants import *
from entities import Player
from entities import Asteroid
from entities import AsteroidField 
from entities import Shot

def main():
    print("Starting Asteroids!")
    print(f"Screen width:",SCREEN_WIDTH)
    print(f"Screen height:",SCREEN_HEIGHT)

    drawables = pygame.sprite.Group()    
    updatable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawables)
    Player.containers = (updatable, drawables)
    Shot.containers = (shots, updatable, drawables)
    AsteroidField.containers = (updatable,)
    

# initialize pygame, define screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, PLAYER_RADIUS, shots)
    asteroid_field = AsteroidField()
    dt = 0

# infinite loop to run the game window
    while True:
        dt = clock.tick(60) / 1000 # limit framerate to 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)

        for asteroid in asteroids:
            if player.collision(asteroid):
                print("Game over!")
                pygame.quit()
                sys.exit()
        for asteroid in asteroids:
            for shot in shots:
                if shot.collision(asteroid):
                    shot.kill()
                    asteroid.split()
                    break
            
        screen.fill("black")

        for drawable in drawables:
            drawable.draw(screen)
       
        pygame.display.flip()


if __name__ == "__main__":
    main()