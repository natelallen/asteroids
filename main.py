#imports
import pygame, sys
from constants import *
from entities import Player
from entities import Asteroid
from entities import AsteroidField 
from entities import Shot
from entities import Scoreboard
from entities import Mainmenu

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
    

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, PLAYER_RADIUS, shots)
    scoreboard = Scoreboard()
    mainmenu = Mainmenu()
    asteroid_field = AsteroidField()
    dt = 0
    game = False 
    background = pygame.image.load("assets/background.png")


# This function is setup to reset the game state if the player wants to play again.
    def reset_game():
        drawables = pygame.sprite.Group()
        updatable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()


        Asteroid.containers = (asteroids, updatable, drawables)
        Player.containers = (updatable, drawables)
        Shot.containers = (shots, updatable, drawables)
        AsteroidField.containers = (updatable,)
        Scoreboard.containers = (drawables,)

        player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, PLAYER_RADIUS, shots)
        asteroid_field = AsteroidField()
        scoreboard = Scoreboard()
        score = 0
        return drawables, updatable, asteroids, shots, player, asteroid_field, scoreboard, score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_n]:
                game = True
        
        
            screen.fill("black")
            mainmenu.draw(screen)
            pygame.display.flip()
            

        while game == True:
            dt = clock.tick(60) / 1000 # limit framerate to 60 fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            updatable.update(dt)

            for asteroid in asteroids:
                if player.collision(asteroid):
                    print("Game over!")
                    drawables, updatable, asteroids, shots, player, asteroid_field, scoreboard, score = reset_game()
                    updatable.update(dt)
                    game = False
                    screen.fill("black")
                    
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collision(asteroid):
                        shot.kill()
                        asteroid.split()
                        scoreboard.add()
                        break
                
            screen.fill("black")
            screen.blit(background, (0, 0))
            for drawable in drawables:
                drawable.draw(screen)
            scoreboard.draw(screen)
            pygame.display.flip()


if __name__ == "__main__":
    main()