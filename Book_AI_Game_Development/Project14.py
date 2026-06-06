# ============================================================
# Project 14: Zombie Survival AI
# Scary Zombie + Dynamic Background + Yellow Moon Version
# ============================================================

import pygame
import random
import math

pygame.init()

WIDTH = 1000
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival AI")

PLAYER_COLOR = (33, 150, 243)
ZOMBIE_COLOR = (75, 150, 85)
ZOMBIE_DARK = (40, 90, 50)
BULLET_COLOR = (255, 214, 64)

TEXT_COLOR = (245, 245, 245)
WHITE = (255, 255, 255)
RED = (255, 40, 40)
DARK_RED = (140, 0, 0)

font = pygame.font.SysFont("arial", 30)
big_font = pygame.font.SysFont("arial", 60)

player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 42, 42)
player_speed = 5

bullets = []
bullet_speed = 11

zombies = []
zombie_spawn_timer = 0
zombie_spawn_delay = 45

score = 0
game_over = False
frame = 0

fog_particles = []

for _ in range(70):
    fog_particles.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3),
        random.uniform(0.2, 0.8)
    ])

clock = pygame.time.Clock()


class Zombie:
    def __init__(self):
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

        self.speed = random.uniform(1.5, 2.4)
        self.radius = 22

    def move(self):
        global game_over

        dx = player.centerx - self.x
        dy = player.centery - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance

        zombie_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

        if zombie_rect.colliderect(player):
            game_over = True

    def draw(self):
        x = int(self.x)
        y = int(self.y)

        # Shadow
        pygame.draw.ellipse(
            screen,
            (20, 20, 25),
            (x - 22, y + 16, 44, 14)
        )

        # Body/head
        pygame.draw.circle(screen, ZOMBIE_DARK, (x + 4, y + 4), self.radius)
        pygame.draw.circle(screen, ZOMBIE_COLOR, (x, y), self.radius)

        # Cracked head lines
        pygame.draw.line(screen, DARK_RED, (x - 8, y - 18), (x - 2, y - 8), 2)
        pygame.draw.line(screen, DARK_RED, (x + 8, y - 18), (x + 3, y - 6), 2)

        # Glowing eyes
        pygame.draw.circle(screen, RED, (x - 8, y - 5), 6)
        pygame.draw.circle(screen, RED, (x + 8, y - 5), 6)
        pygame.draw.circle(screen, WHITE, (x - 8, y - 5), 2)
        pygame.draw.circle(screen, WHITE, (x + 8, y - 5), 2)

        # Angry eyebrows
        pygame.draw.line(screen, DARK_RED, (x - 15, y - 13), (x - 4, y - 8), 3)
        pygame.draw.line(screen, DARK_RED, (x + 15, y - 13), (x + 4, y - 8), 3)

        # Mouth
        pygame.draw.rect(
            screen,
            (25, 10, 10),
            (x - 11, y + 8, 22, 9),
            border_radius=4
        )

        # Teeth
        pygame.draw.polygon(
            screen,
            WHITE,
            [(x - 8, y + 9), (x - 4, y + 9), (x - 6, y + 15)]
        )

        pygame.draw.polygon(
            screen,
            WHITE,
            [(x + 3, y + 9), (x + 7, y + 9), (x + 5, y + 15)]
        )


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - x
        dy = mouse_y - y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            distance = 1

        self.dx = dx / distance
        self.dy = dy / distance
        self.radius = 6

    def move(self):
        self.x += self.dx * bullet_speed
        self.y += self.dy * bullet_speed

    def draw(self):
        pygame.draw.circle(
            screen,
            BULLET_COLOR,
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            2
        )


def reset_game():
    global bullets, zombies, zombie_spawn_timer
    global score, game_over, player, frame

    bullets = []
    zombies = []
    zombie_spawn_timer = 0
    score = 0
    game_over = False
    frame = 0
    player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 42, 42)


def draw_dynamic_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(10 + 15 * ratio + 8 * math.sin(frame * 0.02))
        g = int(12 + 18 * ratio + 6 * math.sin(frame * 0.015 + 2))
        b = int(28 + 35 * ratio + 10 * math.sin(frame * 0.018 + 4))

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    # Moving fog/dust particles
    for fog in fog_particles:
        fog[0] += fog[3]
        fog[1] += 0.15

        if fog[0] > WIDTH:
            fog[0] = 0
            fog[1] = random.randint(0, HEIGHT)

        if fog[1] > HEIGHT:
            fog[1] = 0
            fog[0] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            (55, 60, 75),
            (int(fog[0]), int(fog[1])),
            fog[2]
        )

    # Realistic yellow moon
    moon_x = WIDTH - 130
    moon_y = 100

    # Outer glow
    pygame.draw.circle(
        screen,
        (255, 230, 140),
        (moon_x, moon_y),
        52
    )

    # Main moon
    pygame.draw.circle(
        screen,
        (255, 245, 180),
        (moon_x, moon_y),
        42
    )

    # Small craters
    pygame.draw.circle(
        screen,
        (230, 220, 160),
        (moon_x - 10, moon_y - 8),
        6
    )

    pygame.draw.circle(
        screen,
        (225, 215, 155),
        (moon_x + 12, moon_y + 5),
        5
    )

    pygame.draw.circle(
        screen,
        (235, 225, 170),
        (moon_x - 5, moon_y + 15),
        4
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

    player.left = max(0, player.left)
    player.right = min(WIDTH, player.right)
    player.top = max(0, player.top)
    player.bottom = min(HEIGHT, player.bottom)


def draw_player():
    pygame.draw.circle(screen, PLAYER_COLOR, player.center, 24)

    pygame.draw.circle(
        screen,
        WHITE,
        (player.centerx - 7, player.centery - 5),
        5
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (player.centerx + 7, player.centery - 5),
        5
    )

    pygame.draw.circle(
        screen,
        (20, 20, 20),
        (player.centerx - 7, player.centery - 5),
        2
    )

    pygame.draw.circle(
        screen,
        (20, 20, 20),
        (player.centerx + 7, player.centery - 5),
        2
    )


def move_bullets():
    for bullet in bullets[:]:
        bullet.move()

        if (
            bullet.x < 0 or
            bullet.x > WIDTH or
            bullet.y < 0 or
            bullet.y > HEIGHT
        ):
            bullets.remove(bullet)


def move_zombies():
    for zombie in zombies:
        zombie.move()


def check_collisions():
    global score

    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(
            bullet.x - bullet.radius,
            bullet.y - bullet.radius,
            bullet.radius * 2,
            bullet.radius * 2
        )

        for zombie in zombies[:]:
            zombie_rect = pygame.Rect(
                zombie.x - zombie.radius,
                zombie.y - zombie.radius,
                zombie.radius * 2,
                zombie.radius * 2
            )

            if bullet_rect.colliderect(zombie_rect):
                if bullet in bullets:
                    bullets.remove(bullet)

                if zombie in zombies:
                    zombies.remove(zombie)

                score += 1
                break


def draw_ui():
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)

    help_text = font.render(
        "Arrow keys to move | SPACE to shoot toward mouse",
        True,
        TEXT_COLOR
    )

    screen.blit(score_text, (20, 20))
    screen.blit(help_text, (20, 60))


def draw_game_over():
    title = big_font.render("GAME OVER", True, RED)
    final_score = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    restart = font.render("Press R to restart", True, TEXT_COLOR)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 220))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 310))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 360))


running = True

while running:
    frame += 1

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                reset_game()

            if event.key == pygame.K_SPACE and not game_over:
                bullets.append(Bullet(player.centerx, player.centery))

    if not game_over:
        move_player()

        zombie_spawn_timer += 1

        if zombie_spawn_timer >= zombie_spawn_delay:
            zombies.append(Zombie())
            zombie_spawn_timer = 0

        move_bullets()
        move_zombies()
        check_collisions()

    draw_dynamic_background()
    draw_player()

    for bullet in bullets:
        bullet.draw()

    for zombie in zombies:
        zombie.draw()

    draw_ui()

    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()