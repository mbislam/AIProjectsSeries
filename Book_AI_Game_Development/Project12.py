# ============================================================
# Project 12: AI Space Shooter
# ============================================================

import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Space Shooter")

SPACE_TOP = (12, 20, 55)
SPACE_BOTTOM = (24, 45, 95)

PLAYER_COLOR = (33, 150, 243)
ENEMY_COLOR = (244, 67, 54)
LASER_COLOR = (0, 230, 255)
STAR_COLOR = (255, 255, 255)
TEXT_COLOR = (245, 245, 245)
YELLOW = (255, 214, 64)

font = pygame.font.SysFont("arial", 32)
big_font = pygame.font.SysFont("arial", 56)

player = pygame.Rect(WIDTH // 2 - 30, HEIGHT - 80, 60, 45)
player_speed = 7

bullets = []
bullet_speed = 10

enemies = []
enemy_speed_x = 15
enemy_drop_speed = 75
enemy_move_counter = 0
enemy_move_delay = 25

score = 0
game_over = False

stars = []

for _ in range(90):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])

clock = pygame.time.Clock()


def reset_game():
    global player, bullets, enemies, score, game_over
    global enemy_speed_x, enemy_move_counter

    player = pygame.Rect(WIDTH // 2 - 30, HEIGHT - 80, 60, 45)
    bullets = []
    enemies = []
    score = 0
    game_over = False
    enemy_speed_x = 3
    enemy_move_counter = 0

    create_enemies()


def create_enemies():
    enemies.clear()

    for row in range(3):
        for col in range(7):
            x = 120 + col * 95
            y = 70 + row * 70
            enemies.append(pygame.Rect(x, y, 55, 40))


def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(SPACE_TOP[0] * (1 - ratio) + SPACE_BOTTOM[0] * ratio)
        g = int(SPACE_TOP[1] * (1 - ratio) + SPACE_BOTTOM[1] * ratio)
        b = int(SPACE_TOP[2] * (1 - ratio) + SPACE_BOTTOM[2] * ratio)

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, (star[0], star[1]), star[2])

        star[1] += star[2]

        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0
            star[2] = random.randint(1, 3)


def draw_player():
    points = [
        (player.centerx, player.y),
        (player.x, player.bottom),
        (player.right, player.bottom)
    ]

    pygame.draw.polygon(screen, PLAYER_COLOR, points)
    pygame.draw.circle(screen, YELLOW, (player.centerx, player.bottom - 8), 8)


def draw_enemy(enemy):
    pygame.draw.rect(screen, ENEMY_COLOR, enemy, border_radius=10)

    pygame.draw.circle(screen, TEXT_COLOR, (enemy.x + 16, enemy.y + 16), 5)
    pygame.draw.circle(screen, TEXT_COLOR, (enemy.x + 39, enemy.y + 16), 5)


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


def move_bullets():
    for bullet in bullets[:]:
        bullet.y -= bullet_speed

        if bullet.bottom < 0:
            bullets.remove(bullet)


def enemy_ai():
    global enemy_speed_x, enemy_move_counter, game_over

    enemy_move_counter += 1

    if enemy_move_counter < enemy_move_delay:
        return

    enemy_move_counter = 0
    move_down = False

    for enemy in enemies:
        enemy.x += enemy_speed_x

        if enemy.right >= WIDTH - 30 or enemy.left <= 30:
            move_down = True

    if move_down:
        enemy_speed_x *= -1

        for enemy in enemies:
            enemy.y += enemy_drop_speed

    for enemy in enemies:
        if enemy.bottom >= player.top:
            game_over = True


def check_collisions():
    global score

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break


def draw_score():
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    help_text = font.render("Arrow keys to move, SPACE to shoot", True, TEXT_COLOR)

    screen.blit(score_text, (30, 25))
    screen.blit(help_text, (30, 60))


def draw_game_over():
    if len(enemies) == 0:
        message = "You saved the galaxy!"
        color = YELLOW
    else:
        message = "Game Over!"
        color = ENEMY_COLOR

    title = big_font.render(message, True, color)
    restart = font.render("Press R to restart", True, TEXT_COLOR)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 260))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 330))


create_enemies()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                reset_game()

            if event.key == pygame.K_SPACE and not game_over:
                bullet = pygame.Rect(player.centerx - 4, player.y - 15, 8, 18)
                bullets.append(bullet)

    if not game_over:
        move_player()
        move_bullets()
        enemy_ai()
        check_collisions()

        if len(enemies) == 0:
            game_over = True

    draw_background()
    draw_player()

    for bullet in bullets:
        pygame.draw.rect(screen, LASER_COLOR, bullet, border_radius=4)

    for enemy in enemies:
        draw_enemy(enemy)

    draw_score()

    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()