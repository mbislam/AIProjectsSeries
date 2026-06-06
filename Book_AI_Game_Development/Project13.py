# ============================================================
# Project 13: AI Racing Game
# ============================================================

import pygame
import random
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Racing Game")

WHITE = (255, 255, 255)
TEXT_COLOR = (35, 35, 35)
ROAD_COLOR = (55, 55, 55)
ROAD_EDGE = (30, 30, 30)
PLAYER_COLOR = (33, 150, 243)
AI_COLOR = (244, 67, 54)
WINDOW_COLOR = (210, 240, 255)
YELLOW = (255, 214, 64)

font = pygame.font.SysFont("arial", 32)
big_font = pygame.font.SysFont("arial", 56)

road_x = 220
road_width = 360
lane_width = road_width // 3

lanes = [
    road_x + lane_width // 2 - 25,
    road_x + lane_width + lane_width // 2 - 25,
    road_x + 2 * lane_width + lane_width // 2 - 25
]

player_lane = 1
player = pygame.Rect(lanes[player_lane], 470, 50, 80)

ai_lane = random.choice([0, 1, 2])
ai_car = pygame.Rect(lanes[ai_lane], -100, 50, 80)

ai_speed = 6
line_speed = 8
lane_line_y = 0
score = 0
game_over = False

clock = pygame.time.Clock()


def get_dynamic_background(frame):
    r = int(180 + 35 * math.sin(frame * 0.015))
    g = int(220 + 25 * math.sin(frame * 0.012 + 2))
    b = int(245 + 10 * math.sin(frame * 0.018 + 4))
    return (r, g, b)


def reset_game():
    global player_lane, player, ai_lane, ai_car
    global score, game_over

    player_lane = 1
    player = pygame.Rect(lanes[player_lane], 470, 50, 80)

    ai_lane = random.choice([0, 1, 2])
    ai_car = pygame.Rect(lanes[ai_lane], -100, 50, 80)

    score = 0
    game_over = False


def draw_car(car, color):
    pygame.draw.rect(screen, color, car, border_radius=10)

    pygame.draw.rect(
        screen,
        WINDOW_COLOR,
        (car.x + 10, car.y + 12, 30, 20),
        border_radius=5
    )

    pygame.draw.rect(
        screen,
        WINDOW_COLOR,
        (car.x + 10, car.y + 48, 30, 18),
        border_radius=5
    )

    pygame.draw.circle(screen, ROAD_EDGE, (car.x + 5, car.y + 18), 5)
    pygame.draw.circle(screen, ROAD_EDGE, (car.x + 45, car.y + 18), 5)
    pygame.draw.circle(screen, ROAD_EDGE, (car.x + 5, car.y + 62), 5)
    pygame.draw.circle(screen, ROAD_EDGE, (car.x + 45, car.y + 62), 5)


def draw_road():
    pygame.draw.rect(
        screen,
        ROAD_EDGE,
        (road_x - 15, 0, road_width + 30, HEIGHT)
    )

    pygame.draw.rect(
        screen,
        ROAD_COLOR,
        (road_x, 0, road_width, HEIGHT)
    )

    for i in range(1, 3):
        x = road_x + i * lane_width

        for y in range(-80, HEIGHT, 120):
            pygame.draw.rect(
                screen,
                WHITE,
                (x - 5, y + lane_line_y, 10, 70),
                border_radius=4
            )


def move_ai():
    global ai_lane, ai_car, score

    ai_car.y += ai_speed

    if ai_car.y > HEIGHT:
        score += 1

        if random.random() < 0.65:
            ai_lane = player_lane
        else:
            ai_lane = random.choice([0, 1, 2])

        ai_car.x = lanes[ai_lane]
        ai_car.y = -100


def draw_score():
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    help_text = font.render("Use LEFT and RIGHT arrows", True, TEXT_COLOR)

    screen.blit(score_text, (30, 25))
    screen.blit(help_text, (30, 65))


def draw_game_over():
    title = big_font.render("CRASH!", True, AI_COLOR)
    restart = font.render("Press R to restart", True, TEXT_COLOR)
    final_score = font.render(f"Final Score: {score}", True, TEXT_COLOR)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 190))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 270))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 320))


running = True
frame = 0

while running:
    frame += 1

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                reset_game()

            if not game_over:

                if event.key == pygame.K_LEFT and player_lane > 0:
                    player_lane -= 1
                    player.x = lanes[player_lane]

                elif event.key == pygame.K_RIGHT and player_lane < 2:
                    player_lane += 1
                    player.x = lanes[player_lane]

    if not game_over:
        lane_line_y += line_speed

        if lane_line_y >= 120:
            lane_line_y = 0

        move_ai()

        if player.colliderect(ai_car):
            game_over = True

    screen.fill(get_dynamic_background(frame))

    draw_road()
    draw_car(player, PLAYER_COLOR)
    draw_car(ai_car, AI_COLOR)
    draw_score()

    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()