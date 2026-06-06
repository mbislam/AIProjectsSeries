# ============================================================
# Project 02: Keyboard Movement
# 25 AI Game Development Projects for Kids and Teens
# ============================================================

import pygame

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

pygame.display.set_caption("Keyboard Movement")

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------
BACKGROUND_COLOR = (245, 245, 245)
PLAYER_COLOR = (25, 118, 210)

# ------------------------------------------------------------
# Player Settings
# ------------------------------------------------------------
player_x = 375
player_y = 275

player_size = 50
player_speed = 5

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

        # Close window
        if event.type == pygame.QUIT:
            running = False

    # --------------------------------------------------------
    # Get Keyboard Input
    # --------------------------------------------------------
    keys = pygame.key.get_pressed()

    # --------------------------------------------------------
    # Move Player
    # --------------------------------------------------------
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
    # Draw Background
    # --------------------------------------------------------
    screen.fill(BACKGROUND_COLOR)

    # --------------------------------------------------------
    # Draw Player
    # --------------------------------------------------------
    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
        (player_x, player_y, player_size, player_size)
    )

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