import pygame

from src.config import WHITE
from utils import Point


class Player:
    def __init__(self, location: Point, screen: pygame.Surface):
        self.screen = screen
        self.location = location
        self.speed = 4

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.location.y -= self.speed
        if keys[pygame.K_s]:
            self.location.y += self.speed
        if keys[pygame.K_a]:
            self.location.x -= self.speed
        if keys[pygame.K_d]:
            self.location.x += self.speed

    def draw(self):
        pygame.draw.circle(self.screen, WHITE, (int(self.location.x), int(self.location.y)), 10)
