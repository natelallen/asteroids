# imports
import pygame, random
from constants import *

# CircleShape class
# Most game entities will inherit from this class
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass
    def update(self, dt):
        # sub-classes must override
        pass

    def collision(self, other):
        distance = self.position.distance_to(other.position)
        return distance <= (self.radius + other.radius)

# Player class
class Player(CircleShape):
    def __init__(self, x, y, radius, shots_group):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.shots = shots_group
        self.shoot_cooldown = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 1)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt 
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(dt)
        if keys[pygame.K_d]:
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.shoot_cooldown -= dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_cooldown > 0:
            return
        shot_velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = shot_velocity
        self.shots.add(shot)
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

# Shot (bullet) class
class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

class Scoreboard():
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont('monospace', 24) # - find a better font later

    def draw(self, screen):
        txt = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(txt, (10, 10))

    def add(self):
        self.score += 20

    def val(self):
        return self.score
    
class Mainmenu():
    def __init__(self):
        self.font = pygame.font.SysFont('monospace', 25) # - find a better font later

    def draw(self, screen):
        txt = self.font.render("Press [N] for New Game, Press [Q] for Quit", True, (255, 255, 255))
        screen.blit(txt, (10, 10))


# asteroid class
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        velocity1 = self.velocity.rotate(random_angle) * 1.2 
        velocity2 = self.velocity.rotate(-random_angle) * 1.2
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid1.velocity = velocity1
        new_asteroid2.velocity = velocity2

# AsteroidField class
class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)