import math
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Obstacle:
    location: Point
    radius: int


def distance(a: Point, b: Point):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def check_collision(location: Point, obstacles: list[Obstacle]):
    for obs in obstacles:
        if distance(location, obs.location) < obs.radius + 10:  # 10 is the agent/player radius
            return True
    return False
