# ============================================================
# Project 16: Adaptive Difficulty Game
# ============================================================

import pygame
import random
import math

pygame.init()

WIDTH = 950
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adaptive Difficulty Game")

BACKGROUND_TOP = (25, 30, 60)
BACKGROUND_BOTTOM = (70, 90, 150)

PLAYER_COLOR = (33, 150, 243)

ENEMY_COLORS = [
    (255, 99, 71),
    (255, 193, 7),
    (156, 39, 176),
    (76, 175, 80)
]

WHITE = (255, 255, 255)
TEXT_COLOR = (240, 240, 240)

font = pygame.font.SysFont("arial", 30)
big_font = pygame.font.SysFont("arial", 60)

player = pygame.Rect(WIDTH // 2, HEIGHT - 90, 50, 50)
player_speed = 7

enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = 40

score = 0
difficulty_level = 1
game_over = False

clock = pygame.time.Clock()


class Enemy:
    def __init__(self):
        self.size = random.randint(35, 60)
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.color = random.choice(ENEMY_COLORS)

        self.speed = random.uniform(
            2 + difficulty_level * 0.3,
            4 + difficulty_level * 0.5
        )

    def move(self):
        self.y += self.speed

    def draw(self):
        shadow_rect = pygame.Rect(
            self.x + 4,
            self.y + 4,
            self.size,
            self.size
        )

        pygame.draw.rect(
            screen,
            (20, 20, 20),
            shadow_rect,
            border_radius=10
        )

        main_rect = pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

        pygame.draw.rect(
            screen,
            self.color,
            main_rect,
            border_radius=10
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (self.x + 12, self.y + 15),
            4
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (self.x + self.size - 12, self.y + 15),
            4
        )

        pygame.draw.circle(
            screen,
            (20, 20, 20),
            (self.x + 12, self.y + 15),
            2
        )

        pygame.draw.circle(
            screen,
            (20, 20, 20),
            (self.x + self.size - 12, self.y + 15),
            2
        )


def reset_game():
    global player, enemies, enemy_spawn_timer
    global score, difficulty_level, game_over

    player = pygame.Rect(WIDTH // 2, HEIGHT - 90, 50, 50)
    enemies = []
    enemy_spawn_timer = 0
    score = 0
    difficulty_level = 1
    game_over = False


def draw_background():
    current_time = pygame.time.get_ticks()

    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(
            BACKGROUND_TOP[0] * (1 - ratio) +
            BACKGROUND_BOTTOM[0] * ratio
        )

        g = int(
            BACKGROUND_TOP[1] * (1 - ratio) +
            BACKGROUND_BOTTOM[1] * ratio
        )

        b = int(
            BACKGROUND_TOP[2] * (1 - ratio) +
            BACKGROUND_BOTTOM[2] * ratio
        )

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    # Slow blinking background dots
    for i in range(45):
        dot_x = (i * 73) % WIDTH
        dot_y = (i * 97) % HEIGHT

        brightness = 130 + int(
            60 * (
                0.5 + 0.5 * math.sin(current_time * 0.001 + i)
            )
        )

        color = (brightness, brightness, brightness)

        pygame.draw.circle(
            screen,
            color,
            (dot_x, dot_y),
            2
        )


def move_player():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    if keys[pygame.K_UP]:
        player.y -= player_speed

    if keys[pygame.K_DOWN]:
        player.y += player_speed

    player.left = max(0, player.left)
    player.right = min(WIDTH, player.right)
    player.top = max(0, player.top)
    player.bottom = min(HEIGHT, player.bottom)


def draw_player():
    pygame.draw.ellipse(
        screen,
        (20, 20, 30),
        (player.x + 5, player.y + 42, 40, 10)
    )

    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
        player,
        border_radius=12
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (player.x + 15, player.y + 18),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (player.x + 35, player.y + 18),
        5
    )

    pygame.draw.circle(
        screen,
        (20, 20, 20),
        (player.x + 15, player.y + 18),
        2
    )

    pygame.draw.circle(
        screen,
        (20, 20, 20),
        (player.x + 35, player.y + 18),
        2
    )


def move_enemies():
    global game_over, score, difficulty_level

    for enemy in enemies[:]:
        enemy.move()

        enemy_rect = pygame.Rect(
            enemy.x,
            enemy.y,
            enemy.size,
            enemy.size
        )

        if enemy_rect.colliderect(player):
            game_over = True

        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            score += 1
            difficulty_level = 1 + score // 5


def draw_enemies():
    for enemy in enemies:
        enemy.draw()


def draw_ui():
    score_text = font.render(
        f"Score: {score}",
        True,
        TEXT_COLOR
    )

    difficulty_text = font.render(
        f"Difficulty Level: {difficulty_level}",
        True,
        TEXT_COLOR
    )

    help_text = font.render(
        "Avoid enemies as difficulty increases!",
        True,
        TEXT_COLOR
    )

    screen.blit(score_text, (20, 20))
    screen.blit(difficulty_text, (20, 60))
    screen.blit(help_text, (20, 100))


def draw_game_over():
    title = big_font.render(
        "GAME OVER",
        True,
        WHITE
    )

    final_score = font.render(
        f"Final Score: {score}",
        True,
        TEXT_COLOR
    )

    restart = font.render(
        "Press R to Restart",
        True,
        TEXT_COLOR
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 230)
    )

    screen.blit(
        final_score,
        (WIDTH // 2 - final_score.get_width() // 2, 320)
    )

    screen.blit(
        restart,
        (WIDTH // 2 - restart.get_width() // 2, 370)
    )


running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                reset_game()

    if not game_over:
        move_player()

        enemy_spawn_timer += 1

        spawn_delay = max(
            12,
            enemy_spawn_delay - difficulty_level
        )

        if enemy_spawn_timer >= spawn_delay:
            enemies.append(Enemy())
            enemy_spawn_timer = 0

        move_enemies()

    draw_background()
    draw_player()
    draw_enemies()
    draw_ui()

    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()