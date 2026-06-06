# ============================================================
# Project 07: Smart Snake Game with Eyes
# ============================================================

import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Snake Game")

BACKGROUND_COLOR = (255, 248, 220)
SNAKE_COLOR = (76, 175, 80)
FOOD_COLOR = (244, 67, 54)
TEXT_COLOR = (40, 40, 40)
GRID_COLOR = (220, 220, 220)

snake_speed = 10

font = pygame.font.SysFont("arial", 36)
game_over_font = pygame.font.SysFont("arial", 60)

snake = [
    [100, 100],
    [80, 100],
    [60, 100]
]

direction = "RIGHT"

food_x = random.randrange(0, WIDTH, BLOCK_SIZE)
food_y = random.randrange(0, HEIGHT, BLOCK_SIZE)

score = 0
clock = pygame.time.Clock()


def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_snake():
    for index, segment in enumerate(snake):
        pygame.draw.rect(
            screen,
            SNAKE_COLOR,
            (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE),
            border_radius=5
        )

        if index == 0:
            head_x = segment[0]
            head_y = segment[1]

            eye_radius = 3
            eye_color = (255, 255, 255)
            pupil_color = (0, 0, 0)

            if direction == "RIGHT":
                eye1 = (head_x + 14, head_y + 6)
                eye2 = (head_x + 14, head_y + 14)
            elif direction == "LEFT":
                eye1 = (head_x + 6, head_y + 6)
                eye2 = (head_x + 6, head_y + 14)
            elif direction == "UP":
                eye1 = (head_x + 6, head_y + 6)
                eye2 = (head_x + 14, head_y + 6)
            else:
                eye1 = (head_x + 6, head_y + 14)
                eye2 = (head_x + 14, head_y + 14)

            pygame.draw.circle(screen, eye_color, eye1, eye_radius)
            pygame.draw.circle(screen, eye_color, eye2, eye_radius)
            pygame.draw.circle(screen, pupil_color, eye1, 1)
            pygame.draw.circle(screen, pupil_color, eye2, 1)


def draw_food():
    pygame.draw.rect(
        screen,
        FOOD_COLOR,
        (food_x, food_y, BLOCK_SIZE, BLOCK_SIZE),
        border_radius=5
    )


def draw_score():
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 20))


def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, FOOD_COLOR)
    restart_text = font.render("Press R to Restart or Q to Quit", True, TEXT_COLOR)

    screen.blit(
        game_over_text,
        (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80)
    )

    screen.blit(
        restart_text,
        (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10)
    )


def reset_game():
    global snake, direction, food_x, food_y, score

    snake = [
        [100, 100],
        [80, 100],
        [60, 100]
    ]

    direction = "RIGHT"
    food_x = random.randrange(0, WIDTH, BLOCK_SIZE)
    food_y = random.randrange(0, HEIGHT, BLOCK_SIZE)
    score = 0


running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
                    game_over = False
                if event.key == pygame.K_q:
                    running = False

    if not game_over:
        head_x = snake[0][0]
        head_y = snake[0][1]

        if direction == "UP":
            head_y -= BLOCK_SIZE
        if direction == "DOWN":
            head_y += BLOCK_SIZE
        if direction == "LEFT":
            head_x -= BLOCK_SIZE
        if direction == "RIGHT":
            head_x += BLOCK_SIZE

        new_head = [head_x, head_y]
        snake.insert(0, new_head)

        if head_x == food_x and head_y == food_y:
            score += 1
            food_x = random.randrange(0, WIDTH, BLOCK_SIZE)
            food_y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        else:
            snake.pop()

        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            game_over = True

        for segment in snake[1:]:
            if new_head == segment:
                game_over = True

    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_snake()
    draw_food()
    draw_score()

    if game_over:
        show_game_over()

    pygame.display.update()
    clock.tick(snake_speed)

pygame.quit()