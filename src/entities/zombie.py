import math
import random
from typing import TYPE_CHECKING

import pygame

from src.config import BLUE, GREEN, HEIGHT, RED, WIDTH
from utils import Obstacle, Point, check_collision, distance

if TYPE_CHECKING:
    from src.entities.player import Player


class Zombie:
    def __init__(self, screen: pygame.Surface, location: Point, obstacles: list[Obstacle]):
        self.screen = screen
        self.location = location
        self.speed = 2
        self.state = "Hide"
        self.obstacles = obstacles
        self.direction = self.random_direction()
        self.time_in_risk = 0
        self.direction_change_timer = 0

    def random_direction(self):
        angle = random.uniform(0, 2 * math.pi)
        return math.cos(angle), math.sin(angle)

    def bounce(self):
        self.direction = self.random_direction()

    def slide_along_obstacle(self, obstacle: Obstacle):
        # Vector from zombie to obstacle center
        to_obstacle = Point(obstacle.location.x - self.location.x, obstacle.location.y - self.location.y)
        distance_to_obstacle = math.sqrt(to_obstacle.x**2 + to_obstacle.y**2)

        # Normalize the vector
        if distance_to_obstacle > 0:
            to_obstacle.x /= distance_to_obstacle
            to_obstacle.y /= distance_to_obstacle

        # Tangent vector is perpendicular to the normalized vector
        tangent = Point(-to_obstacle.y, to_obstacle.x)

        # Move along the tangent
        self.location.x += tangent.x * self.speed
        self.location.y += tangent.y * self.speed

    def move(self):
        dx, dy = self.direction
        new_position = Point(self.location.x + dx * self.speed, self.location.y + dy * self.speed)

        for obstacle in self.obstacles:
            if distance(new_position, obstacle.location) <= obstacle.radius:
                self.slide_along_obstacle(obstacle)
                return

        if new_position.x <= 0 or new_position.x >= WIDTH or new_position.y <= 0 or new_position.y >= HEIGHT:
            self.bounce()
        else:
            self.location = new_position

    def move_towards(self, target: Point):
        dx, dy = target.x - self.location.x, target.y - self.location.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            dx, dy = dx / dist, dy / dist
        new_position = Point(self.location.x + dx * self.speed, self.location.y + dy * self.speed)

        for obstacle in self.obstacles:
            if distance(new_position, obstacle.location) <= obstacle.radius:
                self.slide_along_obstacle(obstacle)
                return

        if 0 < new_position.x < WIDTH and 0 < new_position.y < HEIGHT:
            self.location = new_position

    def move_away_from(self, target: Point):
        dx, dy = self.location.x - target.x, self.location.y - target.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            dx, dy = dx / dist, dy / dist
        new_position = Point(self.location.x + dx * self.speed, self.location.y + dy * self.speed)

        for obstacle in self.obstacles:
            if distance(new_position, obstacle.location) <= obstacle.radius:
                self.slide_along_obstacle(obstacle)
                return

        if 0 < new_position.x < WIDTH and 0 < new_position.y < HEIGHT:
            self.location = new_position

    def hide(self, player: "Player"):
        # Find the nearest obstacle to hide behind
        closest_obstacle = None
        closest_distance = float("inf")
        for obstacle in self.obstacles:
            d = distance(self.location, obstacle.location)
            if d < closest_distance:
                closest_obstacle = obstacle
                closest_distance = d

        if closest_obstacle:
            # Move to the side of the obstacle opposite the player
            dx = closest_obstacle.location.x - player.location.x
            dy = closest_obstacle.location.y - player.location.y
            hide_point = Point(
                closest_obstacle.location.x + dx / closest_distance * closest_obstacle.radius,
                closest_obstacle.location.y + dy / closest_distance * closest_obstacle.radius,
            )
            self.move_towards(hide_point)

    def risk(self):
        if self.direction_change_timer <= 0:
            self.direction = self.random_direction()
            self.direction_change_timer = 30

        dx, dy = self.direction
        new_position = Point(self.location.x + dx * self.speed, self.location.y + dy * self.speed)

        if (
            new_position.x <= 0
            or new_position.x >= WIDTH
            or new_position.y <= 0
            or new_position.y >= HEIGHT
            or check_collision(new_position, self.obstacles)
        ):
            self.bounce()
        else:
            self.location = new_position

        self.direction_change_timer -= 1

    def attack(self, player):
        self.move_towards(player.location)

    def check_proximity(self, zombies: list["Zombie"]):
        for other in zombies:
            if other != self and distance(self.location, other.location) < 20:  # Threshold for "nearby"
                self.state = "Attack"
                other.state = "Attack"

    def update(self, player: "Player", zombies: list["Zombie"]):
        self.check_proximity(zombies)

        # State transitions
        if self.state == "Hide":
            if random.random() < 0.01:  # Small chance to switch to Risk
                self.state = "Risk"
            else:
                self.hide(player)
        elif self.state == "Risk":
            self.risk()
            self.time_in_risk += 1
            if self.time_in_risk > 100:  # After some time, go back to hiding
                self.state = "Hide"
                self.time_in_risk = 0
        elif self.state == "Attack":
            self.attack(player)
        else:
            self.move()

    def draw(self):
        color = RED if self.state == "Attack" else (GREEN if self.state == "Risk" else BLUE)
        pygame.draw.circle(self.screen, color, (int(self.location.x), int(self.location.y)), 10)
