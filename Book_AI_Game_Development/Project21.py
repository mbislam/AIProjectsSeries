# Project 21: Game Menus and UI Screens

import pygame
import random

pygame.init()

WIDTH = 950
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menus and UI Screens")

BG_TOP = (25, 30, 60)
BG_BOTTOM = (70, 95, 160)

PLAYER = (33, 150, 243)
ENEMY = (244, 67, 54)

BUTTON = (76, 175, 80)
BUTTON_HOVER = (120, 210, 120)

WHITE = (255, 255, 255)
TEXT = (240, 240, 240)
DARK = (30, 30, 40)

title_font = pygame.font.SysFont("arial", 64)
menu_font = pygame.font.SysFont("arial", 34)
small_font = pygame.font.SysFont("arial", 26)

player = pygame.Rect(460, 520, 50, 50)
player_speed = 6

enemies = []
score = 0
enemy_timer = 0

game_state = "menu"

clock = pygame.time.Clock()


class Enemy:
    def __init__(self):
        self.size = random.randint(35, 55)
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(4, 7)

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(
            screen,
            ENEMY,
            (self.x, self.y, self.size, self.size),
            border_radius=10
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (self.x + 12, self.y + 15),
            4
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (self.x + self.size - 12, self.y + 15),
            4
        )


def reset_game():
    global player, enemies, score, enemy_timer, game_state

    player = pygame.Rect(460, 520, 50, 50)
    enemies = []
    score = 0
    enemy_timer = 0
    game_state = "playing"


def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    for i in range(50):
        x = (i * 79) % WIDTH
        y = (i * 53) % HEIGHT

        pygame.draw.circle(
            screen,
            (180, 200, 255),
            (x, y),
            2
        )


def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON

    if rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=14
    )

    label = menu_font.render(text, True, WHITE)

    screen.blit(
        label,
        (
            rect.centerx - label.get_width() // 2,
            rect.centery - label.get_height() // 2
        )
    )


play_button = pygame.Rect(360, 250, 230, 70)
instructions_button = pygame.Rect(360, 350, 230, 70)
quit_button = pygame.Rect(360, 450, 230, 70)

menu_buttons = [
    ("PLAY", play_button),
    ("INSTRUCTIONS", instructions_button),
    ("QUIT", quit_button)
]


def draw_main_menu():
    title = title_font.render("AI GAME HUB", True, WHITE)

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 110)
    )

    for text, rect in menu_buttons:
        draw_button(rect, text)


def draw_instructions():
    title = title_font.render("HOW TO PLAY", True, WHITE)

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 90)
    )

    instructions = [
        "Use arrow keys to move.",
        "Avoid enemy blocks.",
        "Press P to pause.",
        "Survive as long as possible.",
        "Press ESC to return."
    ]

    y = 220

    for line in instructions:
        text = menu_font.render(line, True, TEXT)

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, y)
        )

        y += 65


def move_player():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    if keys[pygame.K_UP]:
        player.y -= player_speed

    if keys[pygame.K_DOWN]:
        player.y += player_speed

    player.left = max(0, player.left)
    player.right = min(WIDTH, player.right)
    player.top = max(0, player.top)
    player.bottom = min(HEIGHT, player.bottom)


def draw_player():
    pygame.draw.ellipse(
        screen,
        DARK,
        (player.x + 6, player.y + 42, 38, 10)
    )

    pygame.draw.rect(
        screen,
        PLAYER,
        player,
        border_radius=12
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (player.x + 15, player.y + 18),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (player.x + 35, player.y + 18),
        5
    )


def update_enemies():
    global enemy_timer, score, game_state

    enemy_timer += 1

    if enemy_timer >= 32:
        enemies.append(Enemy())
        enemy_timer = 0

    for enemy in enemies[:]:
        enemy.move()

        enemy_rect = pygame.Rect(
            enemy.x,
            enemy.y,
            enemy.size,
            enemy.size
        )

        if enemy_rect.colliderect(player):
            game_state = "game_over"

        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            score += 1


def draw_enemies():
    for enemy in enemies:
        enemy.draw()


def draw_game_ui():
    score_text = small_font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    pause_text = small_font.render(
        "Press P to Pause",
        True,
        WHITE
    )

    screen.blit(score_text, (20, 18))
    screen.blit(pause_text, (20, 50))


def draw_pause_screen():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((20, 20, 20))

    screen.blit(overlay, (0, 0))

    title = title_font.render("PAUSED", True, WHITE)

    text = menu_font.render(
        "Press P to continue",
        True,
        WHITE
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 240)
    )

    screen.blit(
        text,
        (WIDTH // 2 - text.get_width() // 2, 340)
    )


def draw_game_over():
    title = title_font.render("GAME OVER", True, ENEMY)

    score_text = menu_font.render(
        f"Final Score: {score}",
        True,
        WHITE
    )

    restart = small_font.render(
        "Press R to restart",
        True,
        WHITE
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 210)
    )

    screen.blit(
        score_text,
        (WIDTH // 2 - score_text.get_width() // 2, 320)
    )

    screen.blit(
        restart,
        (WIDTH // 2 - restart.get_width() // 2, 390)
    )


running = True

while running:
    draw_background()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if play_button.collidepoint(event.pos):
                    reset_game()

                elif instructions_button.collidepoint(event.pos):
                    game_state = "instructions"

                elif quit_button.collidepoint(event.pos):
                    running = False

        elif game_state == "instructions":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"

        elif game_state == "playing":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    game_state = "paused"

        elif game_state == "paused":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    game_state = "playing"

        elif game_state == "game_over":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    reset_game()

    if game_state == "menu":
        draw_main_menu()

    elif game_state == "instructions":
        draw_instructions()

    elif game_state == "playing":
        move_player()
        update_enemies()
        draw_player()
        draw_enemies()
        draw_game_ui()

    elif game_state == "paused":
        draw_player()
        draw_enemies()
        draw_game_ui()
        draw_pause_screen()

    elif game_state == "game_over":
        draw_player()
        draw_enemies()
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()