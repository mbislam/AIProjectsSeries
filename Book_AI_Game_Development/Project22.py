# Project 22: Multilevel Treasure Hunt

import pygame
import random
import math

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multilevel Treasure Hunt")

BG_TOP = (25, 20, 45)
BG_BOTTOM = (70, 100, 170)

PLAYER = (33, 150, 243)
GUARD = (244, 67, 54)

TREASURE = (0, 255, 200)
KEY = (255, 214, 64)
PORTAL = (180, 80, 255)

WALL = (70, 80, 120)

WHITE = (255, 255, 255)
TEXT = (245, 245, 245)
DARK = (20, 20, 30)
GREEN = (76, 175, 80)

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 56)

player = pygame.Rect(80, 100, 42, 42)
player_speed = 5

level = 1
max_level = 3
score = 0

treasures = []
walls = []
guards = []

key_rect = None
portal_rect = None
has_key = False

game_state = "playing"

clock = pygame.time.Clock()


class Guard:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 42, 42)
        self.direction = random.choice(["left", "right"])
        self.speed = 2 + level * 0.3

    def move(self):
        distance = math.sqrt(
            (player.x - self.rect.x) ** 2 +
            (player.y - self.rect.y) ** 2
        )

        if distance < 180:
            if player.x < self.rect.x:
                self.rect.x -= self.speed

            if player.x > self.rect.x:
                self.rect.x += self.speed

            if player.y < self.rect.y:
                self.rect.y -= self.speed

            if player.y > self.rect.y:
                self.rect.y += self.speed

        else:
            if self.direction == "left":
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

            if random.randint(1, 120) == 1:
                self.direction = random.choice(["left", "right"])

        self.rect.left = max(50, self.rect.left)
        self.rect.right = min(WIDTH - 50, self.rect.right)

    def draw(self):
        pygame.draw.ellipse(
            screen,
            DARK,
            (self.rect.x + 4, self.rect.y + 34, 34, 10)
        )

        pygame.draw.rect(
            screen,
            GUARD,
            self.rect,
            border_radius=10
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (self.rect.x + 13, self.rect.y + 15),
            5
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (self.rect.x + 29, self.rect.y + 15),
            5
        )

        pygame.draw.circle(
            screen,
            DARK,
            (self.rect.x + 13, self.rect.y + 15),
            2
        )

        pygame.draw.circle(
            screen,
            DARK,
            (self.rect.x + 29, self.rect.y + 15),
            2
        )


def create_level():
    global treasures, walls, guards, key_rect, portal_rect
    global has_key, player

    treasures = []
    walls = []
    guards = []
    has_key = False

    player = pygame.Rect(80, 100, 42, 42)

    for i in range(8 + level * 3):
        x = random.randint(100, WIDTH - 120)
        y = random.randint(120, HEIGHT - 100)
        treasures.append(pygame.Rect(x, y, 24, 24))

    for i in range(5 + level * 2):
        x = random.randint(100, WIDTH - 220)
        y = random.randint(120, HEIGHT - 180)
        walls.append(pygame.Rect(x, y, 120, 25))

    for i in range(level + 1):
        x = random.randint(250, WIDTH - 100)
        y = random.randint(150, HEIGHT - 120)
        guards.append(Guard(x, y))

    key_rect = pygame.Rect(
        WIDTH - 130,
        HEIGHT - 120,
        28,
        28
    )

    portal_rect = pygame.Rect(
        WIDTH - 110,
        80,
        55,
        75
    )


create_level()


def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    for i in range(55):
        x = (i * 83 + level * 40) % WIDTH
        y = (i * 67) % HEIGHT

        pygame.draw.circle(
            screen,
            (160, 190, 255),
            (x, y),
            2
        )


def move_player():
    old_x = player.x
    old_y = player.y

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    if keys[pygame.K_UP]:
        player.y -= player_speed

    if keys[pygame.K_DOWN]:
        player.y += player_speed

    player.left = max(40, player.left)
    player.right = min(WIDTH - 40, player.right)
    player.top = max(80, player.top)
    player.bottom = min(HEIGHT - 40, player.bottom)

    for wall in walls:
        if player.colliderect(wall):
            player.x = old_x
            player.y = old_y


def draw_player():
    pygame.draw.ellipse(
        screen,
        DARK,
        (player.x + 5, player.y + 35, 34, 10)
    )

    pygame.draw.rect(
        screen,
        PLAYER,
        player,
        border_radius=10
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (player.x + 13, player.y + 15),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (player.x + 29, player.y + 15),
        5
    )


def draw_treasures():
    for treasure in treasures:
        pygame.draw.polygon(
            screen,
            TREASURE,
            [
                (treasure.centerx, treasure.top),
                (treasure.right, treasure.centery),
                (treasure.centerx, treasure.bottom),
                (treasure.left, treasure.centery)
            ]
        )


def draw_walls():
    for wall in walls:
        pygame.draw.rect(
            screen,
            WALL,
            wall,
            border_radius=6
        )


def draw_key():
    pygame.draw.circle(
        screen,
        KEY,
        key_rect.center,
        14
    )

    pygame.draw.rect(
        screen,
        KEY,
        (
            key_rect.x + 12,
            key_rect.y + 10,
            18,
            8
        )
    )


def draw_portal():
    color = PORTAL if has_key else (90, 90, 90)

    pygame.draw.ellipse(
        screen,
        color,
        portal_rect
    )

    pygame.draw.ellipse(
        screen,
        WHITE,
        portal_rect,
        3
    )


def update_game():
    global score, has_key, game_state, level

    for guard in guards:
        guard.move()

        if guard.rect.colliderect(player):
            game_state = "game_over"

    for treasure in treasures[:]:
        if player.colliderect(treasure):
            treasures.remove(treasure)
            score += 10

    if player.colliderect(key_rect):
        has_key = True

    if player.colliderect(portal_rect):
        if has_key and len(treasures) == 0:
            level += 1

            if level > max_level:
                game_state = "win"
            else:
                create_level()


def draw_ui():
    pygame.draw.rect(
        screen,
        (25, 30, 55),
        (0, 0, WIDTH, 65)
    )

    score_text = font.render(
        f"Score: {score}",
        True,
        TEXT
    )

    level_text = font.render(
        f"Level: {level}/{max_level}",
        True,
        TEXT
    )

    key_text = font.render(
        f"Key: {'YES' if has_key else 'NO'}",
        True,
        KEY
    )

    treasure_text = font.render(
        f"Treasures Left: {len(treasures)}",
        True,
        TREASURE
    )

    screen.blit(score_text, (20, 18))
    screen.blit(level_text, (200, 18))
    screen.blit(key_text, (380, 18))
    screen.blit(treasure_text, (550, 18))


def draw_game_over():
    title = big_font.render(
        "GAME OVER",
        True,
        GUARD
    )

    restart = font.render(
        "Press R to restart",
        True,
        TEXT
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 250)
    )

    screen.blit(
        restart,
        (WIDTH // 2 - restart.get_width() // 2, 340)
    )


def draw_win_screen():
    title = big_font.render(
        "TREASURE MASTER!",
        True,
        GREEN
    )

    final_score = font.render(
        f"Final Score: {score}",
        True,
        TEXT
    )

    restart = font.render(
        "Press R to play again",
        True,
        TEXT
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 220)
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
                level = 1
                score = 0
                game_state = "playing"
                create_level()

    draw_background()

    if game_state == "playing":
        move_player()
        update_game()

        draw_walls()
        draw_treasures()
        draw_key()
        draw_portal()

        for guard in guards:
            guard.draw()

        draw_player()
        draw_ui()

    elif game_state == "game_over":
        draw_walls()
        draw_treasures()
        draw_key()
        draw_portal()

        for guard in guards:
            guard.draw()

        draw_player()
        draw_ui()
        draw_game_over()

    elif game_state == "win":
        draw_win_screen()

    pygame.display.update()
    clock.tick(60)

pygame.quit()