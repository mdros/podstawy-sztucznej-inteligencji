import pygame

from src.config import WHITE
from utils import Obstacle, Point, check_collision


class Player:
    def __init__(self, screen: pygame.Surface, location: Point, obstacles: list[Obstacle]):
        self.screen = screen
        self.location = location
        self.speed = 4
        self.obstacles = obstacles

    def move(self):
        keys = pygame.key.get_pressed()
        new_position = Point(self.location.x, self.location.y)
        if keys[pygame.K_w]:
            new_position.y -= self.speed
        if keys[pygame.K_s]:
            new_position.y += self.speed
        if keys[pygame.K_a]:
            new_position.x -= self.speed
        if keys[pygame.K_d]:
            new_position.x += self.speed

        if not check_collision(new_position, self.obstacles):
            self.location = new_position

    def draw(self):
        pygame.draw.circle(self.screen, WHITE, (int(self.location.x), int(self.location.y)), 10)
