# ============================================================
# Project 11: Enemy AI Platformer
# ============================================================

import pygame

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enemy AI Platformer")

BACKGROUND_COLOR = (255, 248, 220)
PLAYER_COLOR = (33, 150, 243)
ENEMY_COLOR = (244, 67, 54)
PLATFORM_COLOR = (90, 90, 90)
GOAL_COLOR = (76, 175, 80)
TEXT_COLOR = (40, 40, 40)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("arial", 34)
big_font = pygame.font.SysFont("arial", 56)

player = pygame.Rect(80, 450, 40, 50)
player_speed = 5
player_y_velocity = 0
gravity = 0.7
jump_power = -14
on_ground = False

enemy = pygame.Rect(650, 460, 45, 45)
enemy_speed = 3
enemy_direction = -1
enemy_state = "patrol"
chase_distance = 260

goal = pygame.Rect(820, 140, 45, 60)

platforms = [
    pygame.Rect(0, 550, 900, 50),
    pygame.Rect(150, 450, 180, 25),
    pygame.Rect(420, 360, 180, 25),
    pygame.Rect(680, 260, 170, 25),
    pygame.Rect(40, 320, 160, 25)
]

game_over = False
win = False

clock = pygame.time.Clock()


def reset_game():
    global player, player_y_velocity, on_ground
    global enemy, enemy_direction, enemy_state
    global game_over, win

    player = pygame.Rect(80, 450, 40, 50)
    player_y_velocity = 0
    on_ground = False

    enemy = pygame.Rect(650, 460, 45, 45)
    enemy_direction = -1
    enemy_state = "patrol"

    game_over = False
    win = False


def apply_gravity():
    global player_y_velocity, on_ground

    player_y_velocity += gravity
    player.y += player_y_velocity
    on_ground = False

    for platform in platforms:
        if player.colliderect(platform) and player_y_velocity >= 0:
            player.bottom = platform.top
            player_y_velocity = 0
            on_ground = True


def move_player():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    if player.left < 0:
        player.left = 0

    if player.right > WIDTH:
        player.right = WIDTH


def enemy_ai():
    global enemy_direction, enemy_state

    distance = abs(player.centerx - enemy.centerx)

    if distance < chase_distance:
        enemy_state = "chase"
    else:
        enemy_state = "patrol"

    if enemy_state == "chase":
        if player.centerx < enemy.centerx:
            enemy.x -= enemy_speed
        elif player.centerx > enemy.centerx:
            enemy.x += enemy_speed
    else:
        enemy.x += enemy_speed * enemy_direction

        if enemy.left < 520:
            enemy_direction = 1

        if enemy.right > 800:
            enemy_direction = -1


def check_status():
    global game_over, win

    if player.colliderect(enemy):
        game_over = True
        win = False

    if player.colliderect(goal):
        game_over = True
        win = True

    if player.top > HEIGHT:
        game_over = True
        win = False


def draw_player():
    pygame.draw.rect(screen, PLAYER_COLOR, player, border_radius=8)

    eye1 = (player.x + 12, player.y + 15)
    eye2 = (player.x + 28, player.y + 15)

    pygame.draw.circle(screen, WHITE, eye1, 4)
    pygame.draw.circle(screen, WHITE, eye2, 4)
    pygame.draw.circle(screen, TEXT_COLOR, eye1, 2)
    pygame.draw.circle(screen, TEXT_COLOR, eye2, 2)


def draw_enemy():
    pygame.draw.rect(screen, ENEMY_COLOR, enemy, border_radius=8)

    eye1 = (enemy.x + 13, enemy.y + 14)
    eye2 = (enemy.x + 31, enemy.y + 14)

    pygame.draw.circle(screen, WHITE, eye1, 4)
    pygame.draw.circle(screen, WHITE, eye2, 4)
    pygame.draw.circle(screen, TEXT_COLOR, eye1, 2)
    pygame.draw.circle(screen, TEXT_COLOR, eye2, 2)

    label = font.render(enemy_state.upper(), True, TEXT_COLOR)
    screen.blit(label, (enemy.x - 20, enemy.y - 40))


def draw_world():
    screen.fill(BACKGROUND_COLOR)

    for platform in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, platform, border_radius=6)

    pygame.draw.rect(screen, GOAL_COLOR, goal, border_radius=8)

    draw_player()
    draw_enemy()


def draw_status():
    if game_over:
        if win:
            message = "You reached the goal!"
            color = GOAL_COLOR
        else:
            message = "Game Over!"
            color = ENEMY_COLOR

        text = big_font.render(message, True, color)
        restart = font.render("Press R to restart", True, TEXT_COLOR)

        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 190))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 270))
    else:
        help_text = font.render(
            "Arrow keys to move, SPACE to jump. Avoid the AI enemy!",
            True,
            TEXT_COLOR
        )
        screen.blit(help_text, (30, 25))


running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                reset_game()

            if event.key == pygame.K_SPACE and on_ground and not game_over:
                player_y_velocity = jump_power

    if not game_over:
        move_player()
        apply_gravity()
        enemy_ai()
        check_status()

    draw_world()
    draw_status()

    pygame.display.update()
    clock.tick(60)

pygame.quit()