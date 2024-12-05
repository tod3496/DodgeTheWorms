import pygame, math

# player constants
PLAYER_SPEED = 5
PLAYER_SIZE = 10

class Player:
    def __init__(self, screen_width, screen_height) -> None:
        self.pos = [screen_width / 2, screen_height / 2]
        self.rect = pygame.Rect(self.pos[0] - PLAYER_SIZE / 2, self.pos[1] - PLAYER_SIZE / 2, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.color = pygame.Color(0, 255, 0)

    def move(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_d] or keys[pygame.K_x] or keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_a] or keys[pygame.K_z] or keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_w] or keys[pygame.K_QUOTE] or keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_s] or keys[pygame.K_SLASH] or keys[pygame.K_DOWN]:
            dy = 1

        if abs(dx) + abs(dy) == 2:
            dx /= math.sqrt(2)
            dy /= math.sqrt(2)

        self.pos[0] += dx * self.speed
        self.pos[1] += dy * self.speed

        self.rect.update(self.pos[0] - PLAYER_SIZE / 2, self.pos[1] - PLAYER_SIZE / 2, PLAYER_SIZE, PLAYER_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)