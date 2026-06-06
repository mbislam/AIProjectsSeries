# ============================================================
# Project 04: Score System
# 25 AI Game Development Projects for Kids and Teens
# ============================================================

import pygame
import random

# ------------------------------------------------------------
# Initialize Pygame
# ------------------------------------------------------------
pygame.init()

# ------------------------------------------------------------
# Window Settings
# ------------------------------------------------------------
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Score System")

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------
BACKGROUND_COLOR = (245, 248, 250)

PLAYER_COLOR = (25, 118, 210)
COIN_COLOR = (255, 193, 7)

TEXT_COLOR = (30, 30, 30)

# ------------------------------------------------------------
# Font
# ------------------------------------------------------------
font = pygame.font.SysFont("arial", 36)

# ------------------------------------------------------------
# Player Settings
# ------------------------------------------------------------
player_size = 50

player_x = 100
player_y = 100

player_speed = 5

# ------------------------------------------------------------
# Coin Settings
# ------------------------------------------------------------
coin_size = 35

coin_x = random.randint(0, WIDTH - coin_size)
coin_y = random.randint(0, HEIGHT - coin_size)

# ------------------------------------------------------------
# Score
# ------------------------------------------------------------
score = 0

# ------------------------------------------------------------
# Clock
# ------------------------------------------------------------
clock = pygame.time.Clock()

# ------------------------------------------------------------
# Game Loop
# ------------------------------------------------------------
running = True

while running:

    # --------------------------------------------------------
    # Check Events
    # --------------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # --------------------------------------------------------
    # Keyboard Input
    # --------------------------------------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    if keys[pygame.K_UP]:
        player_y -= player_speed

    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # --------------------------------------------------------
    # Keep Player Inside Window
    # --------------------------------------------------------
    if player_x < 0:
        player_x = 0

    if player_x > WIDTH - player_size:
        player_x = WIDTH - player_size

    if player_y < 0:
        player_y = 0

    if player_y > HEIGHT - player_size:
        player_y = HEIGHT - player_size

    # --------------------------------------------------------
    # Create Rectangles
    # --------------------------------------------------------
    player_rect = pygame.Rect(
        player_x,
        player_y,
        player_size,
        player_size
    )

    coin_rect = pygame.Rect(
        coin_x,
        coin_y,
        coin_size,
        coin_size
    )

    # --------------------------------------------------------
    # Collision Detection and Score Update
    # --------------------------------------------------------
    if player_rect.colliderect(coin_rect):

        # Increase score
        score += 1

        # Move coin to new random location
        coin_x = random.randint(0, WIDTH - coin_size)
        coin_y = random.randint(0, HEIGHT - coin_size)

    # --------------------------------------------------------
    # Draw Background
    # --------------------------------------------------------
    screen.fill(BACKGROUND_COLOR)

    # --------------------------------------------------------
    # Draw Player
    # --------------------------------------------------------
    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
        player_rect
    )

    # --------------------------------------------------------
    # Draw Coin
    # --------------------------------------------------------
    pygame.draw.circle(
        screen,
        COIN_COLOR,
        (coin_x + coin_size // 2,
         coin_y + coin_size // 2),
        coin_size // 2
    )

    # --------------------------------------------------------
    # Draw Score
    # --------------------------------------------------------
    score_text = font.render(
        f"Score: {score}",
        True,
        TEXT_COLOR
    )

    screen.blit(score_text, (20, 20))

    # --------------------------------------------------------
    # Update Display
    # --------------------------------------------------------
    pygame.display.update()

    # --------------------------------------------------------
    # FPS Control
    # --------------------------------------------------------
    clock.tick(60)

# ------------------------------------------------------------
# Quit Pygame
# ------------------------------------------------------------
pygame.quit()