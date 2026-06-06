# ============================================================
# Project 09: Reaction Trainer
# ============================================================

import pygame
import random
import time

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reaction Trainer")

WAIT_COLOR = (255, 248, 220)
READY_COLOR = (76, 175, 80)
FALSE_START_COLOR = (244, 67, 54)

TEXT_COLOR = (40, 40, 40)
WHITE = (255, 255, 255)

title_font = pygame.font.SysFont("arial", 48)
message_font = pygame.font.SysFont("arial", 34)
result_font = pygame.font.SysFont("arial", 42)

game_state = "waiting"

start_time = 0
reaction_time = 0

wait_time = random.randint(2000, 5000)
timer_start = pygame.time.get_ticks()

clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_state = "waiting"
                wait_time = random.randint(2000, 5000)
                timer_start = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "ready":
                reaction_time = (time.time() - start_time) * 1000
                game_state = "result"

            elif game_state == "waiting":
                game_state = "false_start"

    if game_state == "waiting":
        if current_time - timer_start >= wait_time:
            game_state = "ready"
            start_time = time.time()

    if game_state == "waiting":
        screen.fill(WAIT_COLOR)

        title = title_font.render("Reaction Trainer", True, TEXT_COLOR)
        message = message_font.render(
            "Wait for GREEN then click!",
            True,
            TEXT_COLOR
        )

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 140))
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, 300))

    elif game_state == "ready":
        screen.fill(READY_COLOR)

        message = title_font.render("CLICK NOW!", True, WHITE)
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, 250))

    elif game_state == "result":
        screen.fill(WAIT_COLOR)

        title = title_font.render("Reaction Result", True, TEXT_COLOR)
        result = result_font.render(f"{int(reaction_time)} ms", True, READY_COLOR)
        restart = message_font.render("Press R to play again", True, TEXT_COLOR)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        screen.blit(result, (WIDTH // 2 - result.get_width() // 2, 280))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 400))

    elif game_state == "false_start":
        screen.fill(FALSE_START_COLOR)

        title = title_font.render("Too Early!", True, WHITE)
        restart = message_font.render("Press R to try again", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 340))

    pygame.display.update()
    clock.tick(60)

pygame.quit()