import math

import pygame

from src.config import HEIGHT, RED, WHITE, WIDTH
from src.entities.zombie import Zombie
from utils import Bullet, Obstacle, Point, check_collision, is_zombie_hit


class Player:
    def __init__(self, screen: pygame.Surface, location: Point, obstacles: list[Obstacle]):
        self.screen = screen
        self.location = location
        self.speed = 4
        self.obstacles = obstacles
        self.bullets: list[Bullet] = []

    def move(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude > 0:
            dx = (dx / magnitude) * self.speed
            dy = (dy / magnitude) * self.speed

        new_position = Point(max(0, min(WIDTH, self.location.x + dx)), max(0, min(HEIGHT, self.location.y + dy)))

        if not check_collision(new_position, self.obstacles):
            self.location = new_position

    def shoot(self, mouse_pos):
        dx = mouse_pos[0] - self.location.x
        dy = mouse_pos[1] - self.location.y

        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude > 0:
            dx = dx / magnitude * 8
            dy = dy / magnitude * 8
            bullet_position = Point(self.location.x, self.location.y)
            self.bullets.append(Bullet(position=bullet_position, velocity=pygame.Vector2(dx, dy)))

    def update_bullets(self, zombies: list["Zombie"]):
        for bullet in self.bullets:
            bullet.position.x += bullet.velocity[0]
            bullet.position.y += bullet.velocity[1]

            for zombie in zombies[:]:
                if is_zombie_hit(zombie, bullet):
                    zombies.remove(zombie)
                    self.bullets.remove(bullet)
                    break

            if (
                bullet.position.x < 0
                or bullet.position.x > WIDTH
                or bullet.position.y < 0
                or bullet.position.y > HEIGHT
                or check_collision(bullet.position, self.obstacles)
            ):
                self.bullets.remove(bullet)

    def draw_bullets(self):
        for bullet in self.bullets:
            pygame.draw.circle(self.screen, RED, (int(bullet.position.x), int(bullet.position.y)), 5)

    def draw(self):
        pygame.draw.circle(self.screen, WHITE, (int(self.location.x), int(self.location.y)), 10)
        self.draw_bullets()
