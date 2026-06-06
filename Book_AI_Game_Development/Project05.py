# ============================================================
# Project 05: Sound Effects
# 25 AI Game Development Projects for Kids and Teens
# ============================================================

import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Window settings
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sound Effects")

# Colors
BACKGROUND_COLOR = (245, 248, 250)
PLAYER_COLOR = (25, 118, 210)
COIN_COLOR = (255, 193, 7)
TEXT_COLOR = (30, 30, 30)

# Font
font = pygame.font.SysFont("arial", 36)

# Load sound file
# Make sure coin.wav is inside a folder named "sounds"
coin_sound = pygame.mixer.Sound("sounds/coin.wav")

# Player settings
player_size = 50
player_x = 100
player_y = 100
player_speed = 5

# Coin settings
coin_size = 35
coin_x = random.randint(0, WIDTH - coin_size)
coin_y = random.randint(0, HEIGHT - coin_size)

# Score
score = 0

# Clock
clock = pygame.time.Clock()

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Keep player inside window
    player_x = max(0, min(player_x, WIDTH - player_size))
    player_y = max(0, min(player_y, HEIGHT - player_size))

    # Create rectangles
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)

    # Collision detection
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()

        coin_x = random.randint(0, WIDTH - coin_size)
        coin_y = random.randint(0, HEIGHT - coin_size)

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Draw coin
    pygame.draw.circle(
        screen,
        COIN_COLOR,
        (coin_x + coin_size // 2, coin_y + coin_size // 2),
        coin_size // 2
    )

    # Draw score
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 20))

    # Draw instruction
    info_text = font.render("Collect coins to hear sound!", True, TEXT_COLOR)
    screen.blit(info_text, (20, 65))

    pygame.display.update()
    clock.tick(60)

pygame.quit()