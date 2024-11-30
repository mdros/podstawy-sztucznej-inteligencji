import random

import pygame

from src.config import BLACK, FPS, HEIGHT, WIDTH
from src.entities.player import Player
from src.entities.zombie import Zombie
from utils import Point

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()


def main():
    player = Player(Point(WIDTH // 2, HEIGHT // 2), screen)
    agent = Zombie(Point(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)), screen)

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
        player.draw()
        agent.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
