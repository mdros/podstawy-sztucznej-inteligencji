import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, s_w, s_h):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.move = pygame.math.Vector2()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(round(self.pos.x), round(self.pos.y)))
        self.s_w = s_w
        self.s_h = s_h

    def update(self):
        clock = pygame.time.Clock()
        time_passed = clock.tick(60) / 1000
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.move.x -= 50
        if pressed[pygame.K_RIGHT]:
            self.move.x += 50
        if pressed[pygame.K_UP]:
            self.move.y -= 100
        if pressed[pygame.K_DOWN]:
            self.move.y += 100

        self.pos = self.pos + self.move * time_passed
        self.rect = self.image.get_rect(midbottom=(round(self.pos.x), round(self.pos.y)))

        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.right > self.s_w:
            self.rect.right = self.s_w
            self.pos.x = self.rect.centerx

        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
        if self.rect.bottom > self.s_h:
            self.rect.bottom = self.s_h
            self.pos.y = self.rect.centery
