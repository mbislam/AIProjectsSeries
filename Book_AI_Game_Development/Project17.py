# ============================================================
# Project 17: AI Strategy Game
# Colorful Battle Arena + Fullscreen Toggle Version
# Press F to switch fullscreen/window mode
# ============================================================

import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 650

ROWS = 10
COLS = 10
CELL = 55

GRID_X = 175
GRID_Y = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Strategy Game")

fullscreen = False

BACKGROUND_COLOR = (235, 245, 255)
GRID_COLOR = (180, 200, 220)

PLAYER_COLOR = (33, 150, 243)
AI_COLOR = (244, 67, 54)
ENERGY_COLOR = (255, 214, 64)

TEXT_COLOR = (35, 35, 35)
WHITE = (255, 255, 255)
GREEN = (76, 175, 80)

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 48)

player_pos = [0, 0]
ai_pos = [9, 9]
energy_pos = [random.randint(1, 8), random.randint(1, 8)]

player_health = 5
ai_health = 5

player_energy = 0
ai_energy = 0

message = "Your turn: use arrow keys."

game_over = False
winner = None

clock = pygame.time.Clock()


def reset_game():
    global player_pos, ai_pos, energy_pos
    global player_health, ai_health
    global player_energy, ai_energy
    global message, game_over, winner

    player_pos = [0, 0]
    ai_pos = [9, 9]
    energy_pos = [random.randint(1, 8), random.randint(1, 8)]

    player_health = 5
    ai_health = 5

    player_energy = 0
    ai_energy = 0

    message = "Your turn: use arrow keys."

    game_over = False
    winner = None


def toggle_fullscreen():
    global screen, fullscreen

    fullscreen = not fullscreen

    if fullscreen:
        screen = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.FULLSCREEN
        )
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))


def grid_to_screen(pos):
    row, col = pos

    x = GRID_X + col * CELL
    y = GRID_Y + row * CELL

    return x, y


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def move_position(pos, d_row, d_col):
    new_row = pos[0] + d_row
    new_col = pos[1] + d_col

    if 0 <= new_row < ROWS and 0 <= new_col < COLS:
        pos[0] = new_row
        pos[1] = new_col


def spawn_energy():
    global energy_pos

    while True:
        new_pos = [
            random.randint(0, ROWS - 1),
            random.randint(0, COLS - 1)
        ]

        if new_pos != player_pos and new_pos != ai_pos:
            energy_pos = new_pos
            break


def check_energy():
    global player_energy, ai_energy

    if player_pos == energy_pos:
        player_energy += 1
        spawn_energy()

    if ai_pos == energy_pos:
        ai_energy += 1
        spawn_energy()


def player_attack():
    global ai_health, player_energy, message

    if distance(player_pos, ai_pos) == 1:
        damage = 1 + player_energy

        ai_health -= damage
        player_energy = 0

        message = f"You attacked AI for {damage} damage!"

        return True

    return False


def ai_choose_move_toward(target):
    best_move = ai_pos[:]
    best_distance = distance(ai_pos, target)

    moves = [
        [ai_pos[0] - 1, ai_pos[1]],
        [ai_pos[0] + 1, ai_pos[1]],
        [ai_pos[0], ai_pos[1] - 1],
        [ai_pos[0], ai_pos[1] + 1]
    ]

    random.shuffle(moves)

    for move in moves:
        row, col = move

        if 0 <= row < ROWS and 0 <= col < COLS and move != player_pos:
            new_distance = distance(move, target)

            if new_distance < best_distance:
                best_distance = new_distance
                best_move = move

    ai_pos[0] = best_move[0]
    ai_pos[1] = best_move[1]


def ai_turn():
    global player_health, ai_energy, message

    if distance(ai_pos, player_pos) == 1:
        damage = 1 + ai_energy

        player_health -= damage
        ai_energy = 0

        message = f"AI attacked you for {damage} damage!"

        return

    if ai_energy < 2 and distance(ai_pos, energy_pos) <= 4:
        ai_choose_move_toward(energy_pos)
        message = "AI moved toward energy."

    else:
        ai_choose_move_toward(player_pos)
        message = "AI moved toward you."


def check_game_over():
    global game_over, winner, message

    if player_health <= 0:
        game_over = True
        winner = "AI"
        message = "AI wins!"

    elif ai_health <= 0:
        game_over = True
        winner = "Player"
        message = "You win!"


def draw_grid():
    # Colorful arena background
    screen.fill((220, 245, 255))

    # Decorative soft circles
    pygame.draw.circle(screen, (190, 230, 255), (120, 120), 70)
    pygame.draw.circle(screen, (200, 240, 230), (780, 130), 90)
    pygame.draw.circle(screen, (255, 235, 190), (120, 520), 80)
    pygame.draw.circle(screen, (230, 220, 255), (800, 520), 90)

    # Main board shadow
    board_shadow = pygame.Rect(
        GRID_X + 8,
        GRID_Y + 8,
        COLS * CELL,
        ROWS * CELL
    )

    pygame.draw.rect(
        screen,
        (170, 185, 200),
        board_shadow,
        border_radius=16
    )

    # Board background
    board_rect = pygame.Rect(
        GRID_X,
        GRID_Y,
        COLS * CELL,
        ROWS * CELL
    )

    pygame.draw.rect(
        screen,
        (245, 250, 255),
        board_rect,
        border_radius=16
    )

    # Checker-style grid cells
    for row in range(ROWS):
        for col in range(COLS):
            x = GRID_X + col * CELL
            y = GRID_Y + row * CELL

            rect = pygame.Rect(x, y, CELL, CELL)

            if (row + col) % 2 == 0:
                cell_color = (235, 248, 255)
            else:
                cell_color = (220, 238, 255)

            pygame.draw.rect(
                screen,
                cell_color,
                rect,
                border_radius=5
            )

            pygame.draw.rect(
                screen,
                GRID_COLOR,
                rect,
                1
            )

            # Small decorative dot
            pygame.draw.circle(
                screen,
                (205, 225, 240),
                (x + CELL // 2, y + CELL // 2),
                3
            )


def draw_character(pos, color, label):
    x, y = grid_to_screen(pos)
    center = (x + CELL // 2, y + CELL // 2)

    # Shadow
    pygame.draw.ellipse(
        screen,
        (150, 165, 180),
        (center[0] - 18, center[1] + 17, 36, 8)
    )

    # Character body
    pygame.draw.circle(screen, color, center, 22)

    # Eyes
    pygame.draw.circle(
        screen,
        WHITE,
        (center[0] - 7, center[1] - 5),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (center[0] + 7, center[1] - 5),
        5
    )

    pygame.draw.circle(
        screen,
        TEXT_COLOR,
        (center[0] - 7, center[1] - 5),
        2
    )

    pygame.draw.circle(
        screen,
        TEXT_COLOR,
        (center[0] + 7, center[1] - 5),
        2
    )

    # Label
    text = font.render(label, True, TEXT_COLOR)

    screen.blit(
        text,
        (center[0] - text.get_width() // 2, center[1] + 20)
    )


def draw_energy():
    x, y = grid_to_screen(energy_pos)
    center = (x + CELL // 2, y + CELL // 2)

    # Glow
    pygame.draw.circle(screen, (255, 235, 130), center, 23)

    # Energy core
    pygame.draw.circle(
        screen,
        ENERGY_COLOR,
        center,
        16
    )

    pygame.draw.circle(
        screen,
        WHITE,
        center,
        6
    )


def draw_ui():
    pygame.draw.rect(
        screen,
        (210, 230, 245),
        (0, 0, WIDTH, 45)
    )

    player_text = font.render(
        f"Player HP: {player_health}  Energy: {player_energy}",
        True,
        TEXT_COLOR
    )

    ai_text = font.render(
        f"AI HP: {ai_health}  Energy: {ai_energy}",
        True,
        TEXT_COLOR
    )

    info_text = font.render(
        message,
        True,
        TEXT_COLOR
    )

    screen.blit(player_text, (20, 15))
    screen.blit(ai_text, (620, 15))

    pygame.draw.rect(
        screen,
        (210, 230, 245),
        (0, 595, WIDTH, 55)
    )

    controls = "F = fullscreen | R = restart | SPACE = attack"
    controls_text = font.render(controls, True, TEXT_COLOR)

    screen.blit(info_text, (20, 605))
    screen.blit(
        controls_text,
        (WIDTH - controls_text.get_width() - 20, 605)
    )


def draw_game_over():
    if winner == "Player":
        title = big_font.render("YOU WIN!", True, GREEN)
    else:
        title = big_font.render("AI WINS!", True, AI_COLOR)

    restart = font.render(
        "Press R to restart",
        True,
        TEXT_COLOR
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 260)
    )

    screen.blit(
        restart,
        (WIDTH // 2 - restart.get_width() // 2, 330)
    )


running = True

while running:
    player_moved = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_f:
                toggle_fullscreen()

            if event.key == pygame.K_r:
                reset_game()

            if not game_over:

                if event.key == pygame.K_UP:
                    move_position(player_pos, -1, 0)
                    player_moved = True

                elif event.key == pygame.K_DOWN:
                    move_position(player_pos, 1, 0)
                    player_moved = True

                elif event.key == pygame.K_LEFT:
                    move_position(player_pos, 0, -1)
                    player_moved = True

                elif event.key == pygame.K_RIGHT:
                    move_position(player_pos, 0, 1)
                    player_moved = True

                elif event.key == pygame.K_SPACE:
                    if player_attack():
                        player_moved = True
                    else:
                        message = "Move next to AI before attacking!"

    if player_moved and not game_over:
        check_energy()
        check_game_over()

        if not game_over:
            ai_turn()
            check_energy()
            check_game_over()

    draw_grid()
    draw_energy()
    draw_character(player_pos, PLAYER_COLOR, "YOU")
    draw_character(ai_pos, AI_COLOR, "AI")
    draw_ui()

    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()