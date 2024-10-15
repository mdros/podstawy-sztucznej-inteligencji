import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

p_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    pygame.draw.polygon(
        screen,
        "red",
        (p_pos, pygame.Vector2(p_pos.x + 100, p_pos.y - 200), pygame.Vector2(p_pos.x - 100, p_pos.y + 200)),
        40,
    )

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        p_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        p_pos.y += 300 * dt
    if keys[pygame.K_a]:
        p_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        p_pos.x += 300 * dt

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
