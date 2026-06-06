# ============================================================
# Project 19: Voice-Controlled Game
# ============================================================

import pygame
import random
import threading
import speech_recognition as sr

pygame.init()

WIDTH = 950
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice-Controlled Game")

BACKGROUND_TOP = (30, 35, 70)
BACKGROUND_BOTTOM = (90, 120, 190)

PLAYER_COLOR = (33, 150, 243)

ENEMY_COLORS = [
    (255, 99, 71),
    (255, 193, 7),
    (156, 39, 176),
    (76, 175, 80)
]

WHITE = (255, 255, 255)
TEXT = (245, 245, 245)

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 60)

player = pygame.Rect(WIDTH // 2, HEIGHT - 100, 50, 50)
player_speed = 45

command_text = "Say a command..."

game_over = False
score = 0

clock = pygame.time.Clock()
enemies = []


class Enemy:
    def __init__(self):
        self.size = random.randint(35, 60)
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(3, 6)
        self.color = random.choice(ENEMY_COLORS)

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(
            screen,
            self.color,
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
    global player, enemies, score, game_over, command_text

    player = pygame.Rect(WIDTH // 2, HEIGHT - 100, 50, 50)
    enemies = []
    score = 0
    game_over = False
    command_text = "Say a command..."


def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(
            BACKGROUND_TOP[0] * (1 - ratio) +
            BACKGROUND_BOTTOM[0] * ratio
        )

        g = int(
            BACKGROUND_TOP[1] * (1 - ratio) +
            BACKGROUND_BOTTOM[1] * ratio
        )

        b = int(
            BACKGROUND_TOP[2] * (1 - ratio) +
            BACKGROUND_BOTTOM[2] * ratio
        )

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    for i in range(35):
        x = (i * 91) % WIDTH
        y = (i * 67) % HEIGHT
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)


def draw_player():
    pygame.draw.ellipse(
        screen,
        (20, 20, 30),
        (player.x + 5, player.y + 42, 40, 10)
    )

    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
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


def move_enemies():
    global game_over, score

    for enemy in enemies[:]:
        enemy.move()

        enemy_rect = pygame.Rect(
            enemy.x,
            enemy.y,
            enemy.size,
            enemy.size
        )

        if enemy_rect.colliderect(player):
            game_over = True

        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            score += 1


def draw_enemies():
    for enemy in enemies:
        enemy.draw()


def draw_ui():
    score_text = font.render(f"Score: {score}", True, TEXT)

    voice_text = font.render(
        f"Voice Command: {command_text}",
        True,
        TEXT
    )

    help_text = font.render(
        "Say: left, right, up, down",
        True,
        TEXT
    )

    screen.blit(score_text, (20, 20))
    screen.blit(voice_text, (20, 60))
    screen.blit(help_text, (20, 100))


def draw_game_over():
    title = big_font.render("GAME OVER", True, WHITE)

    restart = font.render(
        "Press R to Restart",
        True,
        TEXT
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 240)
    )

    screen.blit(
        restart,
        (WIDTH // 2 - restart.get_width() // 2, 330)
    )


def listen_for_commands():
    global command_text

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        if game_over:
            continue

        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.2
                )

                audio = recognizer.listen(
                    source,
                    phrase_time_limit=2
                )

            command = recognizer.recognize_google(audio).lower()
            command_text = command

            if "left" in command:
                player.x -= player_speed

            elif "right" in command:
                player.x += player_speed

            elif "up" in command:
                player.y -= player_speed

            elif "down" in command:
                player.y += player_speed

            player.left = max(0, player.left)
            player.right = min(WIDTH, player.right)
            player.top = max(0, player.top)
            player.bottom = min(HEIGHT, player.bottom)

        except:
            pass


voice_thread = threading.Thread(
    target=listen_for_commands,
    daemon=True
)

voice_thread.start()

enemy_timer = 0
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    if not game_over:
        enemy_timer += 1

        if enemy_timer >= 35:
            enemies.append(Enemy())
            enemy_timer = 0

        move_enemies()

    draw_background()
    draw_player()
    draw_enemies()
    draw_ui()

    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()