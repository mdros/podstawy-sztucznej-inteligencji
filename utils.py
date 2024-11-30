import math
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


def distance(a: Point, b: Point):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
