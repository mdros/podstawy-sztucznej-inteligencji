import random
from dataclasses import astuple

import pygame

from src.config import BLACK, FPS, GRAY, HEIGHT, WIDTH
from src.entities.player import Player
from src.entities.zombie import Zombie
from utils import Obstacle, Point, check_collision

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


def create_zombies(screen: pygame.Surface, obstacles: list[Obstacle], num_agents: int) -> list[Zombie]:
    zombies = []
    for _ in range(num_agents):
        location = Point(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        while check_collision(location, obstacles):
            location = Point(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        zombies.append(Zombie(screen, location, obstacles))
    return zombies


def main():
    obstacles = create_obstacles()
    zombies = create_zombies(screen, obstacles, num_agents=5)
    player = Player(screen, Point(WIDTH // 2, HEIGHT // 2), obstacles)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    player.shoot(mouse_pos)

        player.move()
        player.update_bullets(zombies=zombies)

        for zombie in zombies:
            zombie.update(player, zombies)

        screen.fill(BLACK)
        draw_obstacles(obstacles)
        player.draw()
        for zombie in zombies:
            zombie.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
