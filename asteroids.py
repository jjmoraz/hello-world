# Simple Asteroids-like game using Pygame
# The code aims to replicate basic mechanics of the classic Atari 2600 game.
# Movement, shooting, and asteroid splitting are implemented in a simple manner.

import math
import random
import pygame

# Game constants
WIDTH, HEIGHT = 800, 600
SHIP_SIZE = 20
ASTEROID_MIN_SIZE = 20
ASTEROID_MAX_SIZE = 60
ASTEROID_SPEED_RANGE = (1, 3)
BULLET_SPEED = 7

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Python")
clock = pygame.time.Clock()


class Ship:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0
        self.accel = 0.1
        self.friction = 0.99

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle -= 5
        if keys[pygame.K_RIGHT]:
            self.angle += 5
        if keys[pygame.K_UP]:
            rad = math.radians(self.angle)
            self.speed_x += math.cos(rad) * self.accel
            self.speed_y += math.sin(rad) * self.accel

        self.x += self.speed_x
        self.y += self.speed_y

        self.speed_x *= self.friction
        self.speed_y *= self.friction

        # Wrap around screen
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, surface):
        rad = math.radians(self.angle)
        points = [
            (self.x + math.cos(rad) * SHIP_SIZE, self.y + math.sin(rad) * SHIP_SIZE),
            (self.x + math.cos(rad + 140 * math.pi / 180) * SHIP_SIZE,
             self.y + math.sin(rad + 140 * math.pi / 180) * SHIP_SIZE),
            (self.x + math.cos(rad - 140 * math.pi / 180) * SHIP_SIZE,
             self.y + math.sin(rad - 140 * math.pi / 180) * SHIP_SIZE),
        ]
        pygame.draw.polygon(surface, (255, 255, 255), points, 1)

    def shoot(self):
        rad = math.radians(self.angle)
        bx = self.x + math.cos(rad) * SHIP_SIZE
        by = self.y + math.sin(rad) * SHIP_SIZE
        sx = math.cos(rad) * BULLET_SPEED + self.speed_x
        sy = math.sin(rad) * BULLET_SPEED + self.speed_y
        return Bullet(bx, by, sx, sy)


class Asteroid:
    def __init__(self, x=None, y=None, size=None):
        self.size = size or random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        angle = random.random() * 2 * math.pi
        speed = random.uniform(*ASTEROID_SPEED_RANGE)
        self.speed_x = math.cos(angle) * speed
        self.speed_y = math.sin(angle) * speed

    def update(self):
        self.x = (self.x + self.speed_x) % WIDTH
        self.y = (self.y + self.speed_y) % HEIGHT

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.size, 1)

    def split(self):
        if self.size <= ASTEROID_MIN_SIZE:
            return []
        new_size = self.size // 2
        return [Asteroid(self.x, self.y, new_size), Asteroid(self.x, self.y, new_size)]

    def collides_with(self, obj):
        distance = math.hypot(self.x - obj.x, self.y - obj.y)
        return distance < self.size + getattr(obj, 'size', 0)


class Bullet:
    def __init__(self, x, y, sx, sy):
        self.x = x
        self.y = y
        self.speed_x = sx
        self.speed_y = sy
        self.life = 60  # frames
        self.size = 2

    def update(self):
        self.x = (self.x + self.speed_x) % WIDTH
        self.y = (self.y + self.speed_y) % HEIGHT
        self.life -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.size)


ship = Ship()
asteroids = [Asteroid() for _ in range(5)]
bullets = []

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(ship.shoot())

    keys = pygame.key.get_pressed()
    ship.update(keys)

    for asteroid in asteroids:
        asteroid.update()

    for bullet in bullets[:]:
        bullet.update()
        if bullet.life <= 0:
            bullets.remove(bullet)

    # Collision detection
    for asteroid in asteroids[:]:
        if asteroid.collides_with(ship):
            running = False  # End the game on collision
        for bullet in bullets[:]:
            if asteroid.collides_with(bullet):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                asteroids.extend(asteroid.split())
                break

    # Drawing
    screen.fill((0, 0, 0))
    ship.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()

pygame.quit()
