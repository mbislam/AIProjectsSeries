# ============================================================
# Project 10: AI Maze Runner
# ============================================================

import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
TILE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Maze Runner")

BACKGROUND_COLOR = (255, 248, 220)
WALL_COLOR = (45, 45, 45)
PATH_COLOR = (245, 245, 245)
PLAYER_COLOR = (33, 150, 243)
AI_COLOR = (244, 67, 54)
EXIT_COLOR = (76, 175, 80)
TEXT_COLOR = (40, 40, 40)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("arial", 34)
big_font = pygame.font.SysFont("arial", 56)

maze = [
    "11111111111111111111",
    "10000000010000000001",
    "10111111010111111001",
    "10000001010000001001",
    "11111001011111001001",
    "10001000000001000001",
    "10101111111001111101",
    "10100000001000000001",
    "10111110101111111011",
    "10000010100000001001",
    "11111010111111001001",
    "10000010000000000001",
    "11111111111111111111"
]

ROWS = len(maze)
COLS = len(maze[0])

player = [1, 1]
enemy = [18, 11]
exit_cell = [18, 1]

game_over = False
win = False
enemy_move_delay = 20
enemy_counter = 0

clock = pygame.time.Clock()


def reset_game():
    global player, enemy, game_over, win, enemy_counter

    player = [1, 1]
    enemy = [18, 11]
    game_over = False
    win = False
    enemy_counter = 0


def is_path(col, row):
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return False

    return maze[row][col] == "0"


def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE, row * TILE, TILE, TILE)

            if maze[row][col] == "1":
                pygame.draw.rect(screen, WALL_COLOR, rect)
            else:
                pygame.draw.rect(screen, PATH_COLOR, rect)

            pygame.draw.rect(screen, (220, 220, 220), rect, 1)


def draw_objects():
    exit_rect = pygame.Rect(
        exit_cell[0] * TILE + 6,
        exit_cell[1] * TILE + 6,
        TILE - 12,
        TILE - 12
    )

    player_rect = pygame.Rect(
        player[0] * TILE + 6,
        player[1] * TILE + 6,
        TILE - 12,
        TILE - 12
    )

    enemy_rect = pygame.Rect(
        enemy[0] * TILE + 6,
        enemy[1] * TILE + 6,
        TILE - 12,
        TILE - 12
    )

    pygame.draw.rect(screen, EXIT_COLOR, exit_rect, border_radius=8)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect, border_radius=8)
    pygame.draw.rect(screen, AI_COLOR, enemy_rect, border_radius=8)

    eye1 = (enemy_rect.x + 10, enemy_rect.y + 10)
    eye2 = (enemy_rect.x + 22, enemy_rect.y + 10)

    pygame.draw.circle(screen, WHITE, eye1, 4)
    pygame.draw.circle(screen, WHITE, eye2, 4)

    pygame.draw.circle(screen, TEXT_COLOR, eye1, 2)
    pygame.draw.circle(screen, TEXT_COLOR, eye2, 2)


def move_player(dx, dy):
    if game_over:
        return

    new_col = player[0] + dx
    new_row = player[1] + dy

    if is_path(new_col, new_row):
        player[0] = new_col
        player[1] = new_row


def get_ai_moves():
    moves = []
    possible = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dx, dy in possible:
        new_col = enemy[0] + dx
        new_row = enemy[1] + dy

        if is_path(new_col, new_row):
            distance = abs(player[0] - new_col) + abs(player[1] - new_row)
            moves.append((distance, new_col, new_row))

    return moves


def move_enemy():
    moves = get_ai_moves()

    if moves:
        moves.sort()

        best_distance = moves[0][0]

        best_moves = []

        for move in moves:
            if move[0] == best_distance:
                best_moves.append(move)

        chosen = random.choice(best_moves)

        enemy[0] = chosen[1]
        enemy[1] = chosen[2]


def check_game_status():
    global game_over, win

    if player == exit_cell:
        game_over = True
        win = True

    elif player == enemy:
        game_over = True
        win = False


def draw_status():
    panel_y = ROWS * TILE

    pygame.draw.rect(
        screen,
        BACKGROUND_COLOR,
        (0, panel_y, WIDTH, HEIGHT - panel_y)
    )

    if game_over:
        if win:
            message = "You escaped the maze!"
            color = EXIT_COLOR
        else:
            message = "AI caught you!"
            color = AI_COLOR

        text = big_font.render(message, True, color)
        restart = font.render("Press R to restart", True, TEXT_COLOR)

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, panel_y + 15)
        )

        screen.blit(
            restart,
            (WIDTH // 2 - restart.get_width() // 2, panel_y + 80)
        )

    else:
        text = font.render(
            "Reach the green exit before the AI catches you!",
            True,
            TEXT_COLOR
        )

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, panel_y + 40)
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
                if event.key == pygame.K_LEFT:
                    move_player(-1, 0)

                elif event.key == pygame.K_RIGHT:
                    move_player(1, 0)

                elif event.key == pygame.K_UP:
                    move_player(0, -1)

                elif event.key == pygame.K_DOWN:
                    move_player(0, 1)

    if not game_over:
        enemy_counter += 1

        if enemy_counter >= enemy_move_delay:
            move_enemy()
            enemy_counter = 0

        check_game_status()

    screen.fill(BACKGROUND_COLOR)

    draw_maze()
    draw_objects()
    draw_status()

    pygame.display.update()
    clock.tick(60)

pygame.quit()