import random
from dataclasses import astuple

import pygame

from src.config import BLACK, FPS, GRAY, HEIGHT, WIDTH
from src.entities.player import Player
from src.entities.zombie import Zombie
from utils import Obstacle, Point

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()


def create_obstacles() -> list[Obstacle]:
    return [
        Obstacle(Point(200, 300), 40),
        Obstacle(Point(400, 150), 50),
        Obstacle(Point(600, 400), 35),
        Obstacle(Point(300, 500), 45),
        Obstacle(Point(700, 250), 30),
    ]


def draw_obstacles(obstacles: list[Obstacle]):
    for obs in obstacles:
        pygame.draw.circle(screen, GRAY, astuple(obs.location), obs.radius)


def main():
    obstacles = create_obstacles()
    player = Player(screen, Point(WIDTH // 2, HEIGHT // 2), obstacles)
    agent = Zombie(screen, Point(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)), obstacles)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic
        player.move()
        agent.update(player)

        # Drawing
        screen.fill(BLACK)
        draw_obstacles(obstacles)
        player.draw()
        agent.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
