import math
import random

import pygame

from src.config import BLUE, GREEN, HEIGHT, RED, WIDTH
from utils import Obstacle, Point, check_collision, distance


class Zombie:
    def __init__(self, screen: pygame.Surface, location: Point, obstacles: list[Obstacle]):
        self.screen = screen
        self.location = location
        self.speed = 2
        self.state = "Patrol"
        self.waypoints = [Point(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(3)]
        self.current_waypoint = 0
        self.detection_radius = 150
        self.attack_radius = 50
        self.obstacles = obstacles

    def patrol(self):
        # Move towards the current waypoint
        waypoint = self.waypoints[self.current_waypoint]
        if distance(self.location, waypoint) < 5:
            self.current_waypoint = (self.current_waypoint + 1) % len(self.waypoints)
        else:
            self.move_towards(waypoint)

    def chase(self, player):
        self.move_towards(player.location)

    def attack(self):
        pass  # For simplicity, we won't implement attack mechanics in detail

    def move_towards(self, target: Point):
        dx, dy = target.x - self.location.x, target.y - self.location.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            dx, dy = dx / dist, dy / dist
        new_position = Point(self.location.x + dx * self.speed, self.location.y + dy * self.speed)
        if not check_collision(new_position, self.obstacles):
            self.location = new_position

    def update(self, player):
        # State transitions
        if self.state == "Patrol":
            if distance(self.location, player.location) < self.detection_radius:
                self.state = "Chase"
            self.patrol()
        elif self.state == "Chase":
            if distance(self.location, player.location) < self.attack_radius:
                self.state = "Attack"
            elif distance(self.location, player.location) > self.detection_radius:
                self.state = "Patrol"
            self.chase(player)
        elif self.state == "Attack":
            if distance(self.location, player.location) > self.attack_radius:
                self.state = "Chase"
            self.attack()

    def draw(self):
        color = RED if self.state == "Attack" else (GREEN if self.state == "Chase" else BLUE)
        pygame.draw.circle(self.screen, color, (int(self.location.x), int(self.location.y)), 10)
