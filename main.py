import pygame

from entities.player import Player

pygame.init()
screen = pygame.display.set_mode((1920, 1080))


player = Player(1920 / 2, 1080 / 2, s_w=1920, s_h=1080)
allSprites = pygame.sprite.Group(player)

clock = pygame.time.Clock()
while True:
    time_passed = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    allSprites.update()
    screen.fill((220, 220, 255))
    allSprites.draw(screen)
    pygame.display.flip()
