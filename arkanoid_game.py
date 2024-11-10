import pygame
import random
import sys

# Inicjalizacja Pygame:
pygame.init()

# Wymiary ekranu:
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid")

# Kolory:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 200)

# Paletka:
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

# Piłka:
BALL_SIZE = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = -4

# Cegiełka:
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_COLOR = [RED, GREEN, BLUE]

# Poziomy:
LEVELS = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Dodaj więcej poziomów w podobnym formacie:
]

# Klasa Paletka:
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - PADDLE_WIDTH//2, SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= PADDLE_SPEED
        if direction == "right" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PADDLE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

# Klasa Piłka:
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self):
        self.rect.x = SCREEN_WIDTH//2 - BALL_SIZE//2
        self.rect.y = SCREEN_HEIGHT//2 - BALL_SIZE//2
        self.speed_x *= random.choice([-1, 1])
        self.speed_y *= random.choice([-1, 1])

# Klasa Cegiełka:
class Brick:
    def __init__(self, x, y, level):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = BRICK_COLOR[level % len(BRICK_COLOR)]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)

# Klasa Przycisk:
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = BUTTON_COLOR

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, pos):
        if self.is_clicked(pos):
            self.color = BUTTON_HOVER_COLOR
        else:
            self.color = BUTTON_COLOR

# Klasa Gra:
class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.level = 0
        self.bricks = self.create_level(self.level)
        self.running = True

        self.restart_level_button = Button("RESTART POZIOMU", 50, 10, 200, 40, self.restart_level)
        self.restart_game_button = Button("RESTART CAŁEJ GRY", 400, 10, 200, 40, self.restart_game)

    def create_level(self, level):
        bricks = []
        level_data = LEVELS[level]
        for row in range(len(level_data)):
            for col in range(len(level_data[row])):
                if level_data[row][col] == 1:
                    bricks.append(Brick(col * (BRICK_WIDTH + 10) + 35, row * (BRICK_HEIGHT + 10) + 70, level))
        return bricks

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_level_button.is_clicked(event.pos):
                        self.restart_level_button.action()
                    if self.restart_game_button.is_clicked(event.pos):
                        self.restart_game_button.action()

            pos = pygame.mouse.get_pos()
            self.restart_level_button.update(pos)
            self.restart_game_button.update(pos)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT]:
                self.paddle.move("right")

            self.ball.move()
            self.check_collisions()

            SCREEN.fill(BLACK)
            self.paddle.draw(SCREEN)
            self.ball.draw(SCREEN)
            for brick in self.bricks:
                brick.draw(SCREEN)

            self.restart_level_button.draw(SCREEN)
            self.restart_game_button.draw(SCREEN)

            pygame.display.flip()
            clock.tick(60)

    def check_collisions(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed_y *= -1

        for brick in self.bricks:
            if self.ball.rect.colliderect(brick.rect):
                self.bricks.remove(brick)
                self.ball.speed_y *= -1
                break

        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.ball.reset()
            self.paddle.rect.x = SCREEN_WIDTH//2 - PADDLE_WIDTH//2

        if not self.bricks:
            self.level += 1
            if self.level >= len(LEVELS):
                self.running = False
            else:
                self.bricks = self.create_level(self.level)

    def restart_level(self):
        self.ball.reset()
        self.paddle.rect.x = SCREEN_WIDTH//2 - PADDLE_WIDTH//2
        self.bricks = self.create_level(self.level)

    def restart_game(self):
        self.level = 0
        self.ball.reset()
        self.paddle.rect.x = SCREEN_WIDTH//2 - PADDLE_WIDTH//2
        self.bricks = self.create_level(self.level)

# Rozpoczęcie gry:
if __name__ == "__main__":
    Game().run()
    pygame.quit()
    sys.exit()
