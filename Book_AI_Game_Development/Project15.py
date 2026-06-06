# ============================================================
# Project 15: Pathfinding Game
# ============================================================

import pygame
from collections import deque

pygame.init()

WIDTH = 900
HEIGHT = 650
ROWS = 13
COLS = 18
CELL = 45

GRID_X = 45
GRID_Y = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Game")

BACKGROUND_COLOR = (225, 240, 255)
GRID_COLOR = (190, 205, 220)
WALL_COLOR = (45, 45, 55)
OPEN_COLOR = (245, 250, 255)
VISITED_COLOR = (180, 220, 255)
PATH_COLOR = (255, 214, 64)
ROBOT_COLOR = (33, 150, 243)
TARGET_COLOR = (76, 175, 80)
TEXT_COLOR = (35, 35, 35)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 44)

grid = [
    "000000000000000000",
    "011111001111100010",
    "000001000000100010",
    "011101111110101110",
    "010000000010100000",
    "010111111010111110",
    "010100001010000010",
    "000101101011111010",
    "011100100000001010",
    "000000111111101010",
    "011110000000001000",
    "000010111111111110",
    "000000000000000000"
]

robot_pos = (0, 0)
target_pos = None
path = []
visited_cells = []
robot_step_delay = 12
robot_step_counter = 0
message = "Click an open cell to set a target."

clock = pygame.time.Clock()


def reset_robot():
    global robot_pos, target_pos, path, visited_cells, message

    robot_pos = (0, 0)
    target_pos = None
    path = []
    visited_cells = []
    message = "Click an open cell to set a target."


def clear_path():
    global target_pos, path, visited_cells, message

    target_pos = None
    path = []
    visited_cells = []
    message = "Path cleared. Click a new target."


def is_open(row, col):
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return False

    return grid[row][col] == "0"


def bfs(start, goal):
    queue = deque([start])
    came_from = {start: None}
    visited_order = []

    while queue:
        current = queue.popleft()
        visited_order.append(current)

        if current == goal:
            break

        row, col = current

        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        for neighbor in neighbors:
            n_row, n_col = neighbor

            if is_open(n_row, n_col) and neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current

    if goal not in came_from:
        return [], visited_order

    final_path = []
    current = goal

    while current is not None:
        final_path.append(current)
        current = came_from[current]

    final_path.reverse()

    return final_path, visited_order


def cell_from_mouse(pos):
    mouse_x, mouse_y = pos

    col = (mouse_x - GRID_X) // CELL
    row = (mouse_y - GRID_Y) // CELL

    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return None

    return (row, col)


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = GRID_X + col * CELL
            y = GRID_Y + row * CELL

            rect = pygame.Rect(x, y, CELL, CELL)

            if grid[row][col] == "1":
                color = WALL_COLOR
            else:
                color = OPEN_COLOR

            if (row, col) in visited_cells:
                color = VISITED_COLOR

            if (row, col) in path:
                color = PATH_COLOR

            if target_pos == (row, col):
                color = TARGET_COLOR

            pygame.draw.rect(screen, color, rect, border_radius=4)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def draw_robot():
    row, col = robot_pos

    x = GRID_X + col * CELL + CELL // 2
    y = GRID_Y + row * CELL + CELL // 2

    pygame.draw.circle(screen, ROBOT_COLOR, (x, y), 18)
    pygame.draw.rect(
        screen,
        ROBOT_COLOR,
        (x - 14, y + 8, 28, 12),
        border_radius=4
    )

    pygame.draw.circle(screen, WHITE, (x - 7, y - 4), 5)
    pygame.draw.circle(screen, WHITE, (x + 7, y - 4), 5)

    pygame.draw.circle(screen, TEXT_COLOR, (x - 7, y - 4), 2)
    pygame.draw.circle(screen, TEXT_COLOR, (x + 7, y - 4), 2)

    pygame.draw.line(screen, TEXT_COLOR, (x - 9, y - 18), (x - 14, y - 28), 3)
    pygame.draw.line(screen, TEXT_COLOR, (x + 9, y - 18), (x + 14, y - 28), 3)

    pygame.draw.circle(screen, TARGET_COLOR, (x - 14, y - 30), 4)
    pygame.draw.circle(screen, TARGET_COLOR, (x + 14, y - 30), 4)


def draw_ui():

    # Top panel background
    pygame.draw.rect(
        screen,
        (210, 225, 240),
        (0, 0, WIDTH, 70)
    )

    # Title
    title = big_font.render(
        "Pathfinding Game",
        True,
        TEXT_COLOR
    )

    # Message
    info = font.render(
        message,
        True,
        TEXT_COLOR
    )

    # Controls
    controls = font.render(
        "R = reset robot   C = clear path",
        True,
        TEXT_COLOR
    )

    # Draw text
    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 5)
    )

    screen.blit(info, (20, 45))

    screen.blit(
        controls,
        (WIDTH - controls.get_width() - 20, 45)
    )


def move_robot_along_path():
    global robot_pos, path, robot_step_counter, message

    if len(path) <= 1:
        return

    robot_step_counter += 1

    if robot_step_counter >= robot_step_delay:
        robot_step_counter = 0
        path.pop(0)
        robot_pos = path[0]

        if len(path) == 1:
            message = "Robot reached the target!"


running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_robot()

            elif event.key == pygame.K_c:
                clear_path()

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_cell = cell_from_mouse(pygame.mouse.get_pos())

            if clicked_cell and is_open(clicked_cell[0], clicked_cell[1]):
                target_pos = clicked_cell
                path, visited_cells = bfs(robot_pos, target_pos)

                if path:
                    message = "Path found! Robot is moving."
                else:
                    message = "No path found."

    move_robot_along_path()

    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_robot()
    draw_ui()

    pygame.display.update()
    clock.tick(60)

pygame.quit()