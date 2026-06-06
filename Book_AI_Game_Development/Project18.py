# Project 18: Smart NPC Behavior

import pygame
import math

pygame.init()

WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart NPC Behavior")

PLAYER = (33, 150, 243)
FRIEND = (76, 175, 80)
PATROL = (255, 152, 0)
GUARD = (244, 67, 54)
TEXT = (35, 35, 35)
WHITE = (255, 255, 255)
ROAD = (200, 210, 220)
GRASS = (185, 230, 180)
WATER = (120, 200, 240)
HOUSE = (230, 180, 120)

font = pygame.font.SysFont("arial", 26)
big_font = pygame.font.SysFont("arial", 54)

player = pygame.Rect(90, 300, 42, 42)
player_speed = 5
game_over = False
message = "Explore the town. Avoid the red guard!"

clock = pygame.time.Clock()


class NPC:
    def __init__(self, x, y, color, role):
        self.rect = pygame.Rect(x, y, 42, 42)
        self.start_x = x
        self.start_y = y
        self.color = color
        self.role = role
        self.state = "idle"
        self.speed = 2
        self.direction = 1

    def distance_to_player(self):
        dx = player.centerx - self.rect.centerx
        dy = player.centery - self.rect.centery
        return math.sqrt(dx * dx + dy * dy)

    def move_toward_player(self, speed):
        dx = player.centerx - self.rect.centerx
        dy = player.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            self.rect.x += int(speed * dx / distance)
            self.rect.y += int(speed * dy / distance)

    def patrol_move(self):
        self.rect.x += self.speed * self.direction

        if self.rect.x > self.start_x + 140:
            self.direction = -1

        if self.rect.x < self.start_x - 80:
            self.direction = 1

    def update(self):
        global game_over, message

        distance = self.distance_to_player()

        if self.role == "friend":
            if distance < 180:
                self.state = "follow"
                self.move_toward_player(1.5)
            else:
                self.state = "idle"

        elif self.role == "patrol":
            self.state = "patrol"
            self.patrol_move()

        elif self.role == "guard":
            if distance < 230:
                self.state = "chase"
                self.move_toward_player(2.6)
                message = "Guard is chasing you!"
            else:
                self.state = "watch"
                self.patrol_move()

            if self.rect.colliderect(player):
                game_over = True
                message = "The guard caught you!"

    def draw(self):
        pygame.draw.ellipse(
            screen,
            (120, 140, 140),
            (self.rect.x + 4, self.rect.y + 34, 34, 10)
        )

        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=10
        )

        pygame.draw.circle(screen, WHITE, (self.rect.x + 13, self.rect.y + 16), 5)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 29, self.rect.y + 16), 5)

        pygame.draw.circle(screen, TEXT, (self.rect.x + 13, self.rect.y + 16), 2)
        pygame.draw.circle(screen, TEXT, (self.rect.x + 29, self.rect.y + 16), 2)

        label = font.render(self.state.upper(), True, TEXT)
        screen.blit(
            label,
            (self.rect.centerx - label.get_width() // 2, self.rect.y - 28)
        )


npcs = [
    NPC(300, 150, FRIEND, "friend"),
    NPC(370, 440, FRIEND, "friend"),
    NPC(530, 250, PATROL, "patrol"),
    NPC(690, 410, PATROL, "patrol"),
    NPC(770, 170, GUARD, "guard")
]


def reset_game():
    global player, game_over, message, npcs

    player = pygame.Rect(90, 300, 42, 42)
    game_over = False
    message = "Explore the town. Avoid the red guard!"

    npcs = [
        NPC(300, 150, FRIEND, "friend"),
        NPC(370, 440, FRIEND, "friend"),
        NPC(530, 250, PATROL, "patrol"),
        NPC(690, 410, PATROL, "patrol"),
        NPC(770, 170, GUARD, "guard")
    ]


def draw_world():
    screen.fill(GRASS)

    pygame.draw.rect(screen, ROAD, (0, 285, WIDTH, 80))
    pygame.draw.rect(screen, ROAD, (430, 0, 80, HEIGHT))

    pygame.draw.circle(screen, WATER, (120, 120), 70)
    pygame.draw.circle(screen, (150, 220, 250), (120, 120), 45)

    pygame.draw.rect(screen, HOUSE, (620, 70, 120, 90), border_radius=8)
    pygame.draw.polygon(screen, (170, 90, 70), [(600, 70), (680, 20), (760, 70)])

    pygame.draw.rect(screen, (240, 200, 140), (160, 465, 130, 90), border_radius=8)
    pygame.draw.polygon(screen, (170, 90, 70), [(140, 465), (225, 410), (310, 465)])

    pygame.draw.circle(screen, (120, 190, 120), (830, 540), 45)
    pygame.draw.rect(screen, (120, 80, 40), (820, 540, 20, 55))


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
        (100, 120, 130),
        (player.x + 4, player.y + 34, 34, 10)
    )

    pygame.draw.rect(
        screen,
        PLAYER,
        player,
        border_radius=10
    )

    pygame.draw.circle(screen, WHITE, (player.x + 13, player.y + 16), 5)
    pygame.draw.circle(screen, WHITE, (player.x + 29, player.y + 16), 5)

    pygame.draw.circle(screen, TEXT, (player.x + 13, player.y + 16), 2)
    pygame.draw.circle(screen, TEXT, (player.x + 29, player.y + 16), 2)

    label = font.render("PLAYER", True, TEXT)
    screen.blit(
        label,
        (player.centerx - label.get_width() // 2, player.y - 28)
    )


def draw_ui():
    pygame.draw.rect(screen, (230, 245, 235), (0, 0, WIDTH, 45))

    info = font.render(message, True, TEXT)
    controls = font.render("Arrow keys = move | R = restart", True, TEXT)

    screen.blit(info, (20, 13))
    screen.blit(controls, (WIDTH - controls.get_width() - 20, 13))


def draw_game_over():
    title = big_font.render("CAUGHT!", True, GUARD)
    restart = font.render("Press R to restart", True, TEXT)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 250))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 325))


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

        for npc in npcs:
            npc.update()

    draw_world()

    for npc in npcs:
        npc.draw()

    draw_player()
    draw_ui()

    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()