# Project 23: Boss Battle AI

import pygame
import random
import math

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Battle AI")

BG_TOP = (20, 15, 45)
BG_BOTTOM = (70, 40, 120)

PLAYER = (33, 150, 243)
BOSS = (180, 40, 220)
BOSS_DARK = (90, 20, 120)

PLAYER_BULLET = (255, 214, 64)
BOSS_BULLET = (255, 80, 80)

WHITE = (255, 255, 255)
TEXT = (245, 245, 245)
DARK = (20, 20, 30)
GREEN = (76, 175, 80)
RED = (244, 67, 54)
YELLOW = (255, 214, 64)

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 60)

player = pygame.Rect(WIDTH // 2, HEIGHT - 90, 46, 46)
player_speed = 6
player_health = 6

boss = pygame.Rect(WIDTH // 2 - 70, 90, 140, 90)
boss_health = 100
boss_direction = 1
boss_phase = 1

player_bullets = []
boss_bullets = []

shoot_cooldown = 0
boss_attack_timer = 0

game_state = "playing"
message = "Defeat the AI boss!"

clock = pygame.time.Clock()


class Bullet:
    def __init__(self, x, y, dx, dy, color, speed, radius):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.speed = speed
        self.radius = radius

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            max(2, self.radius // 2)
        )


def reset_game():
    global player, player_health
    global boss, boss_health, boss_direction, boss_phase
    global player_bullets, boss_bullets
    global shoot_cooldown, boss_attack_timer
    global game_state, message

    player = pygame.Rect(WIDTH // 2, HEIGHT - 90, 46, 46)
    player_health = 6

    boss = pygame.Rect(WIDTH // 2 - 70, 90, 140, 90)
    boss_health = 100
    boss_direction = 1
    boss_phase = 1

    player_bullets = []
    boss_bullets = []

    shoot_cooldown = 0
    boss_attack_timer = 0

    game_state = "playing"
    message = "Defeat the AI boss!"


def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    for i in range(60):
        x = (i * 79 + pygame.time.get_ticks() // 40) % WIDTH
        y = (i * 53) % HEIGHT

        pygame.draw.circle(
            screen,
            (110, 90, 180),
            (x, y),
            2
        )

    pygame.draw.rect(
        screen,
        (40, 35, 80),
        (45, 80, WIDTH - 90, HEIGHT - 130),
        3,
        border_radius=18
    )


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

    player.left = max(50, player.left)
    player.right = min(WIDTH - 50, player.right)
    player.top = max(220, player.top)
    player.bottom = min(HEIGHT - 50, player.bottom)


def draw_player():
    pygame.draw.ellipse(
        screen,
        DARK,
        (player.x + 4, player.y + 38, 38, 10)
    )

    pygame.draw.rect(
        screen,
        PLAYER,
        player,
        border_radius=12
    )

    pygame.draw.circle(screen, WHITE, (player.x + 14, player.y + 18), 5)
    pygame.draw.circle(screen, WHITE, (player.x + 32, player.y + 18), 5)

    pygame.draw.circle(screen, DARK, (player.x + 14, player.y + 18), 2)
    pygame.draw.circle(screen, DARK, (player.x + 32, player.y + 18), 2)

    pygame.draw.rect(
        screen,
        PLAYER_BULLET,
        (player.centerx - 4, player.y - 10, 8, 18),
        border_radius=3
    )


def update_boss_phase():
    global boss_phase, message

    if boss_health > 65:
        boss_phase = 1
        message = "Boss Phase 1: Slow attack pattern."
    elif boss_health > 30:
        boss_phase = 2
        message = "Boss Phase 2: Faster attacks!"
    else:
        boss_phase = 3
        message = "Boss Phase 3: Final rage mode!"


def move_boss():
    global boss_direction

    speed = 2 + boss_phase
    boss.x += speed * boss_direction

    if boss.left < 80:
        boss.left = 80
        boss_direction = 1

    if boss.right > WIDTH - 80:
        boss.right = WIDTH - 80
        boss_direction = -1


def boss_attack():
    global boss_attack_timer

    boss_attack_timer += 1
    attack_delay = max(22, 70 - boss_phase * 15)

    if boss_attack_timer >= attack_delay:
        boss_attack_timer = 0

        if boss_phase == 1:
            boss_bullets.append(
                Bullet(
                    boss.centerx,
                    boss.bottom,
                    0,
                    1,
                    BOSS_BULLET,
                    5,
                    8
                )
            )

        elif boss_phase == 2:
            for dx in [-0.35, 0, 0.35]:
                boss_bullets.append(
                    Bullet(
                        boss.centerx,
                        boss.bottom,
                        dx,
                        1,
                        BOSS_BULLET,
                        5.5,
                        8
                    )
                )

        else:
            for dx in [-0.6, -0.3, 0, 0.3, 0.6]:
                boss_bullets.append(
                    Bullet(
                        boss.centerx,
                        boss.bottom,
                        dx,
                        1,
                        BOSS_BULLET,
                        6,
                        8
                    )
                )


def shoot_player_bullet():
    global shoot_cooldown

    if shoot_cooldown <= 0:
        player_bullets.append(
            Bullet(
                player.centerx,
                player.top,
                0,
                -1,
                PLAYER_BULLET,
                9,
                6
            )
        )

        shoot_cooldown = 12


def update_bullets():
    global boss_health, player_health, game_state

    for bullet in player_bullets[:]:
        bullet.move()

        if bullet.y < 0:
            player_bullets.remove(bullet)

        elif bullet.rect().colliderect(boss):
            player_bullets.remove(bullet)
            boss_health -= 4

            if boss_health <= 0:
                boss_health = 0
                game_state = "win"

    for bullet in boss_bullets[:]:
        bullet.move()

        if bullet.y > HEIGHT:
            boss_bullets.remove(bullet)

        elif bullet.rect().colliderect(player):
            boss_bullets.remove(bullet)
            player_health -= 1

            if player_health <= 0:
                player_health = 0
                game_state = "game_over"


def draw_boss():
    pygame.draw.ellipse(
        screen,
        DARK,
        (boss.x + 15, boss.y + 80, 110, 18)
    )

    pygame.draw.rect(
        screen,
        BOSS_DARK,
        (boss.x + 8, boss.y + 8, boss.width, boss.height),
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        BOSS,
        boss,
        border_radius=18
    )

    pygame.draw.circle(screen, WHITE, (boss.x + 40, boss.y + 35), 10)
    pygame.draw.circle(screen, WHITE, (boss.x + 100, boss.y + 35), 10)

    pygame.draw.circle(screen, RED, (boss.x + 40, boss.y + 35), 5)
    pygame.draw.circle(screen, RED, (boss.x + 100, boss.y + 35), 5)

    pygame.draw.rect(
        screen,
        DARK,
        (boss.x + 35, boss.y + 62, 70, 12),
        border_radius=5
    )

    if boss_phase == 3:
        pygame.draw.circle(
            screen,
            YELLOW,
            boss.center,
            80,
            3
        )


def draw_health_bars():
    pygame.draw.rect(screen, DARK, (40, 20, 260, 25), border_radius=8)

    pygame.draw.rect(
        screen,
        GREEN,
        (40, 20, int(260 * player_health / 6), 25),
        border_radius=8
    )

    player_label = font.render("Player", True, TEXT)
    screen.blit(player_label, (40, 50))

    pygame.draw.rect(screen, DARK, (WIDTH - 340, 20, 300, 25), border_radius=8)

    pygame.draw.rect(
        screen,
        RED,
        (WIDTH - 340, 20, int(300 * boss_health / 100), 25),
        border_radius=8
    )

    boss_label = font.render(f"Boss Phase {boss_phase}", True, TEXT)
    screen.blit(boss_label, (WIDTH - 340, 50))


def draw_ui():
    info = font.render(message, True, TEXT)

    help_text = font.render(
        "Arrow keys = move | SPACE = shoot | R = restart",
        True,
        TEXT
    )

    screen.blit(info, (40, HEIGHT - 55))

    screen.blit(
        help_text,
        (WIDTH - help_text.get_width() - 40, HEIGHT - 55)
    )


def draw_game_over():
    title = big_font.render("BOSS WINS!", True, RED)
    restart = font.render("Press R to restart", True, TEXT)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 300))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 375))


def draw_win_screen():
    title = big_font.render("YOU DEFEATED THE BOSS!", True, GREEN)
    restart = font.render("Press R to play again", True, TEXT)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 300))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 375))


running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                reset_game()

            if event.key == pygame.K_SPACE and game_state == "playing":
                shoot_player_bullet()

    if game_state == "playing":
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        move_player()
        update_boss_phase()
        move_boss()
        boss_attack()
        update_bullets()

    draw_background()
    draw_boss()
    draw_player()

    for bullet in player_bullets:
        bullet.draw()

    for bullet in boss_bullets:
        bullet.draw()

    draw_health_bars()
    draw_ui()

    if game_state == "game_over":
        draw_game_over()

    if game_state == "win":
        draw_win_screen()

    pygame.display.update()
    clock.tick(60)

pygame.quit()