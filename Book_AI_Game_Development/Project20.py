# Project 20: AI Survival Arena

import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Survival Arena")

BG_TOP = (20, 25, 55)
BG_BOTTOM = (55, 75, 120)

PLAYER = (33, 150, 243)
ENEMY = (244, 67, 54)
FAST_ENEMY = (255, 112, 67)

HEALTH = (76, 175, 80)
SHIELD = (255, 214, 64)

WHITE = (255, 255, 255)
TEXT = (245, 245, 245)
DARK = (25, 25, 35)

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 60)

player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 46, 46)
player_speed = 6

enemies = []
powerups = []

score = 0
health = 5
wave = 1
shield_timer = 0
game_over = False

enemy_spawn_timer = 0
powerup_timer = 0

clock = pygame.time.Clock()


class EnemyAI:
    def __init__(self, fast=False):
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            self.x = random.randint(0, WIDTH)
            self.y = -40

        elif side == "bottom":
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + 40

        elif side == "left":
            self.x = -40
            self.y = random.randint(0, HEIGHT)

        else:
            self.x = WIDTH + 40
            self.y = random.randint(0, HEIGHT)

        self.fast = fast
        self.radius = 18 if fast else 22

        if fast:
            self.speed = random.uniform(2.0, 3.0)
        else:
            self.speed = random.uniform(1.2, 2.0)

        self.color = FAST_ENEMY if fast else ENEMY

    def move(self):
        dx = player.centerx - self.x
        dy = player.centery - self.y

        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def draw(self):
        x = int(self.x)
        y = int(self.y)

        pygame.draw.ellipse(
            screen,
            DARK,
            (x - self.radius, y + 12, self.radius * 2, 12)
        )

        pygame.draw.circle(screen, self.color, (x, y), self.radius)

        pygame.draw.circle(screen, WHITE, (x - 7, y - 5), 5)
        pygame.draw.circle(screen, WHITE, (x + 7, y - 5), 5)

        pygame.draw.circle(screen, DARK, (x - 7, y - 5), 2)
        pygame.draw.circle(screen, DARK, (x + 7, y - 5), 2)

        if self.fast:
            pygame.draw.line(
                screen,
                SHIELD,
                (x - 12, y + 10),
                (x + 12, y + 10),
                3
            )


class PowerUp:
    def __init__(self):
        self.kind = random.choice(["health", "shield"])
        self.x = random.randint(70, WIDTH - 70)
        self.y = random.randint(90, HEIGHT - 70)
        self.radius = 17

    def rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def draw(self):
        color = HEALTH if self.kind == "health" else SHIELD

        pygame.draw.circle(
            screen,
            WHITE,
            (self.x, self.y),
            self.radius + 6
        )

        pygame.draw.circle(
            screen,
            color,
            (self.x, self.y),
            self.radius
        )

        if self.kind == "health":
            pygame.draw.rect(
                screen,
                WHITE,
                (self.x - 4, self.y - 11, 8, 22)
            )

            pygame.draw.rect(
                screen,
                WHITE,
                (self.x - 11, self.y - 4, 22, 8)
            )

        else:
            pygame.draw.polygon(
                screen,
                WHITE,
                [
                    (self.x, self.y - 12),
                    (self.x + 12, self.y - 2),
                    (self.x + 8, self.y + 12),
                    (self.x, self.y + 16),
                    (self.x - 8, self.y + 12),
                    (self.x - 12, self.y - 2)
                ]
            )


def reset_game():
    global player, enemies, powerups
    global score, health, wave, shield_timer, game_over
    global enemy_spawn_timer, powerup_timer

    player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 46, 46)

    enemies = []
    powerups = []

    score = 0
    health = 5
    wave = 1
    shield_timer = 0
    game_over = False

    enemy_spawn_timer = 0
    powerup_timer = 0


def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    for i in range(60):
        x = (i * 83 + score * 2) % WIDTH
        y = (i * 47) % HEIGHT

        pygame.draw.circle(
            screen,
            (90, 110, 160),
            (x, y),
            2
        )

    pygame.draw.rect(
        screen,
        (35, 45, 75),
        (40, 130, WIDTH - 80, HEIGHT - 180),
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

    player.left = max(45, player.left)
    player.right = min(WIDTH - 45, player.right)
    player.top = max(130, player.top)
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

    pygame.draw.circle(
        screen,
        WHITE,
        (player.x + 15, player.y + 18),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (player.x + 31, player.y + 18),
        5
    )

    pygame.draw.circle(
        screen,
        DARK,
        (player.x + 15, player.y + 18),
        2
    )

    pygame.draw.circle(
        screen,
        DARK,
        (player.x + 31, player.y + 18),
        2
    )

    if shield_timer > 0:
        pygame.draw.circle(
            screen,
            SHIELD,
            player.center,
            36,
            4
        )


def spawn_enemies():
    global enemy_spawn_timer

    enemy_spawn_timer += 1

    spawn_delay = max(14, 55 - wave * 4)

    if enemy_spawn_timer >= spawn_delay:
        fast = random.random() < min(0.35, wave * 0.05)
        enemies.append(EnemyAI(fast))
        enemy_spawn_timer = 0


def update_wave():
    global wave

    wave = 1 + score // 10


def move_enemies():
    global health, game_over, shield_timer

    for enemy in enemies[:]:
        enemy.move()

        if enemy.rect().colliderect(player):
            enemies.remove(enemy)

            if shield_timer > 0:
                shield_timer = max(0, shield_timer - 60)
            else:
                health -= 1

            if health <= 0:
                game_over = True


def spawn_powerups():
    global powerup_timer

    powerup_timer += 1

    if powerup_timer >= 260:
        powerups.append(PowerUp())
        powerup_timer = 0

    if len(powerups) > 4:
        powerups.pop(0)


def collect_powerups():
    global health, shield_timer, score

    for powerup in powerups[:]:
        if powerup.rect().colliderect(player):
            powerups.remove(powerup)

            if powerup.kind == "health":
                health = min(8, health + 1)
            else:
                shield_timer = 240

            score += 2


def update_score():
    global score

    if pygame.time.get_ticks() % 30 == 0:
        score += 1


def draw_ui():
    panel = pygame.Rect(0, 0, WIDTH, 95)

    pygame.draw.rect(screen, (30, 40, 70), panel)

    score_text = font.render(f"Score: {score}", True, TEXT)
    health_text = font.render(f"Health: {health}", True, TEXT)
    wave_text = font.render(f"Wave: {wave}", True, TEXT)

    if shield_timer > 0:
        shield_text = font.render("Shield: ON", True, SHIELD)
    else:
        shield_text = font.render("Shield: OFF", True, TEXT)

    help_text = font.render(
        "Arrow keys = move | Collect power-ups | R = restart",
        True,
        TEXT
    )

    screen.blit(score_text, (20, 18))
    screen.blit(health_text, (180, 18))
    screen.blit(wave_text, (340, 18))
    screen.blit(shield_text, (480, 18))
    screen.blit(help_text, (20, 55))


def draw_game_over():
    title = big_font.render("SURVIVAL ENDED", True, ENEMY)
    final_score = font.render(f"Final Score: {score}", True, TEXT)
    final_wave = font.render(f"Highest Wave: {wave}", True, TEXT)
    restart = font.render("Press R to restart", True, TEXT)

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 230)
    )

    screen.blit(
        final_score,
        (WIDTH // 2 - final_score.get_width() // 2, 315)
    )

    screen.blit(
        final_wave,
        (WIDTH // 2 - final_wave.get_width() // 2, 355)
    )

    screen.blit(
        restart,
        (WIDTH // 2 - restart.get_width() // 2, 400)
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
        move_player()
        spawn_enemies()
        move_enemies()
        spawn_powerups()
        collect_powerups()
        update_score()
        update_wave()

        if shield_timer > 0:
            shield_timer -= 1

    draw_background()
    draw_player()

    for powerup in powerups:
        powerup.draw()

    for enemy in enemies:
        enemy.draw()

    draw_ui()

    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()