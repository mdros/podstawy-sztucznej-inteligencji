import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pygame import Vector2

if TYPE_CHECKING:
    from src.entities.zombie import Zombie


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Obstacle:
    location: Point
    radius: int


@dataclass
class Bullet:
    position: Point
    velocity: Vector2


def is_zombie_hit(zombie: "Zombie", bullet: Bullet) -> bool:
    return distance(zombie.location, bullet.position) < 10


def distance(a: Point, b: Point):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def check_collision(location: Point, obstacles: list[Obstacle]):
    for obs in obstacles:
        if distance(location, obs.location) < obs.radius + 10:  # 10 is the agent/player radius
            return True
    return False
