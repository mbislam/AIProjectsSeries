# ============================================================
# Project 03: Collision Detection
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

pygame.display.set_caption("Collision Detection")

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------
BACKGROUND_COLOR = (240, 240, 240)

PLAYER_COLOR = (25, 118, 210)
TARGET_COLOR = (229, 57, 53)

TEXT_COLOR = (0, 0, 0)

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
# Target Settings
# ------------------------------------------------------------
target_size = 40

target_x = random.randint(0, WIDTH - target_size)
target_y = random.randint(0, HEIGHT - target_size)

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
    # Events
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

    target_rect = pygame.Rect(
        target_x,
        target_y,
        target_size,
        target_size
    )

    # --------------------------------------------------------
    # Collision Detection
    # --------------------------------------------------------
    if player_rect.colliderect(target_rect):

        # Increase score
        score += 1

        # Move target
        target_x = random.randint(0, WIDTH - target_size)
        target_y = random.randint(0, HEIGHT - target_size)

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
    # Draw Target
    # --------------------------------------------------------
    pygame.draw.rect(
        screen,
        TARGET_COLOR,
        target_rect
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