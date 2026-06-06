# ============================================================
# Project 06: AI Tic-Tac-Toe
# 25 AI Game Development Projects for Kids and Teens
# ============================================================

import pygame
import random

pygame.init()

# ------------------------------------------------------------
# Window Settings
# ------------------------------------------------------------
WIDTH = 600
HEIGHT = 700
BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Tic-Tac-Toe")

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------
BACKGROUND_COLOR = (255, 248, 220)
GRID_COLOR = (40, 40, 40)
PLAYER_COLOR = (25, 118, 210)
AI_COLOR = (229, 57, 53)
TEXT_COLOR = (30, 30, 30)

# ------------------------------------------------------------
# Fonts
# ------------------------------------------------------------
font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 28)

# ------------------------------------------------------------
# Game Variables
# ------------------------------------------------------------
player = "X"
ai = "O"

board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]

current_turn = player
winner = None
game_over = False


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------
def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(
            screen, GRID_COLOR,
            (0, i * CELL_SIZE),
            (BOARD_SIZE, i * CELL_SIZE),
            5
        )

        pygame.draw.line(
            screen, GRID_COLOR,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, BOARD_SIZE),
            5
        )


def draw_marks():
    for row in range(3):
        for col in range(3):
            mark = board[row][col]

            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2

            if mark == "X":
                offset = 50
                pygame.draw.line(
                    screen, PLAYER_COLOR,
                    (center_x - offset, center_y - offset),
                    (center_x + offset, center_y + offset),
                    8
                )
                pygame.draw.line(
                    screen, PLAYER_COLOR,
                    (center_x + offset, center_y - offset),
                    (center_x - offset, center_y + offset),
                    8
                )

            elif mark == "O":
                pygame.draw.circle(
                    screen, AI_COLOR,
                    (center_x, center_y),
                    60,
                    8
                )


def check_winner(mark):
    # Check rows
    for row in range(3):
        if (
            board[row][0] == mark and
            board[row][1] == mark and
            board[row][2] == mark
        ):
            return True

    # Check columns
    for col in range(3):
        if (
            board[0][col] == mark and
            board[1][col] == mark and
            board[2][col] == mark
        ):
            return True

    # Check diagonals
    if (
        board[0][0] == mark and
        board[1][1] == mark and
        board[2][2] == mark
    ):
        return True

    if (
        board[0][2] == mark and
        board[1][1] == mark and
        board[2][0] == mark
    ):
        return True

    return False


def board_full():
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                return False
    return True


def get_empty_cells():
    empty_cells = []

    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                empty_cells.append((row, col))

    return empty_cells


def find_winning_move(mark):
    for row, col in get_empty_cells():
        board[row][col] = mark

        if check_winner(mark):
            board[row][col] = ""
            return (row, col)

        board[row][col] = ""

    return None


def ai_move():
    # Rule 1: Win if possible
    move = find_winning_move(ai)
    if move:
        return move

    # Rule 2: Block player if player can win
    move = find_winning_move(player)
    if move:
        return move

    # Rule 3: Take center
    if board[1][1] == "":
        return (1, 1)

    # Rule 4: Take corner
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    available_corners = []

    for corner in corners:
        row, col = corner
        if board[row][col] == "":
            available_corners.append(corner)

    if available_corners:
        return random.choice(available_corners)

    # Rule 5: Pick any empty cell
    empty_cells = get_empty_cells()
    if empty_cells:
        return random.choice(empty_cells)

    return None


def draw_status():
    pygame.draw.rect(
        screen,
        BACKGROUND_COLOR,
        (0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE)
    )

    if game_over:
        if winner == player:
            message = "You win!"
        elif winner == ai:
            message = "AI wins!"
        else:
            message = "It's a tie!"

        restart_message = "Press R to restart"

        text = font.render(message, True, TEXT_COLOR)
        restart_text = small_font.render(restart_message, True, TEXT_COLOR)

        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 615))
        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, 660)
        )

    else:
        if current_turn == player:
            message = "Your turn: click a square"
        else:
            message = "AI is thinking..."

        text = small_font.render(message, True, TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 635))


def reset_game():
    global board, current_turn, winner, game_over

    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

    current_turn = player
    winner = None
    game_over = False


# ------------------------------------------------------------
# Main Game Loop
# ------------------------------------------------------------
clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if mouse_y < BOARD_SIZE and current_turn == player:
                row = mouse_y // CELL_SIZE
                col = mouse_x // CELL_SIZE

                if board[row][col] == "":
                    board[row][col] = player

                    if check_winner(player):
                        winner = player
                        game_over = True
                    elif board_full():
                        winner = None
                        game_over = True
                    else:
                        current_turn = ai

    # AI turn
    if current_turn == ai and not game_over:
        move = ai_move()

        if move:
            row, col = move
            board[row][col] = ai

            if check_winner(ai):
                winner = ai
                game_over = True
            elif board_full():
                winner = None
                game_over = True
            else:
                current_turn = player

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_marks()
    draw_status()

    pygame.display.update()
    clock.tick(60)

pygame.quit()