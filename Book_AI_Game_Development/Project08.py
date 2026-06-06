# ============================================================
# Project 08: AI Quiz Battle
# Colorful Buttons + Randomized Answer Positions
# ============================================================

import pygame
import random

pygame.init()

# ------------------------------------------------------------
# Window Settings
# ------------------------------------------------------------
WIDTH = 900
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Quiz Battle")

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------
BACKGROUND_COLOR = (255, 248, 220)

TEXT_COLOR = (40, 40, 40)
WHITE = (255, 255, 255)

OPTION_COLORS = [
    (33, 150, 243),    # Blue
    (76, 175, 80),     # Green
    (255, 152, 0),     # Orange
    (156, 39, 176)     # Purple
]

OPTION_HOVER_COLORS = [
    (66, 165, 245),    # Light Blue
    (102, 187, 106),   # Light Green
    (255, 183, 77),    # Light Orange
    (186, 104, 200)    # Light Purple
]

CORRECT_COLOR = (76, 175, 80)
WRONG_COLOR = (244, 67, 54)

# ------------------------------------------------------------
# Fonts
# ------------------------------------------------------------
title_font = pygame.font.SysFont("arial", 42)
question_font = pygame.font.SysFont("arial", 32)
option_font = pygame.font.SysFont("arial", 28)
score_font = pygame.font.SysFont("arial", 30)

# ------------------------------------------------------------
# Quiz Questions
# correct_answer stores the actual text answer
# ------------------------------------------------------------
questions = [
    {
        "question": "What does AI stand for?",
        "options": [
            "Artificial Intelligence",
            "Automatic Internet",
            "Amazing Interface",
            "Advanced Input"
        ],
        "correct_answer": "Artificial Intelligence"
    },
    {
        "question": "Which language is popular for AI?",
        "options": [
            "Python",
            "HTML",
            "CSS",
            "PowerPoint"
        ],
        "correct_answer": "Python"
    },
    {
        "question": "Which library is used in this book?",
        "options": [
            "Pygame",
            "Photoshop",
            "Excel",
            "Word"
        ],
        "correct_answer": "Pygame"
    },
    {
        "question": "What is used to store game score?",
        "options": [
            "Variable",
            "Folder",
            "Monitor",
            "Speaker"
        ],
        "correct_answer": "Variable"
    },
    {
        "question": "Which key moves the player up?",
        "options": [
            "Arrow Up",
            "Shift",
            "Tab",
            "Escape"
        ],
        "correct_answer": "Arrow Up"
    }
]

# ------------------------------------------------------------
# Shuffle Answer Choices for Each Question
# ------------------------------------------------------------
for question in questions:
    random.shuffle(question["options"])

# ------------------------------------------------------------
# Game Variables
# ------------------------------------------------------------
current_question = 0
player_score = 0
ai_score = 0
game_over = False

feedback_message = ""
feedback_color = TEXT_COLOR

# ------------------------------------------------------------
# Button Rectangles
# ------------------------------------------------------------
buttons = []

for i in range(4):
    rect = pygame.Rect(150, 220 + i * 90, 600, 60)
    buttons.append(rect)


# ------------------------------------------------------------
# AI Answer Function
# ------------------------------------------------------------
def ai_answer(correct_answer, options):
    # AI answers correctly 70% of the time
    if random.random() < 0.7:
        return correct_answer

    wrong_options = []

    for option in options:
        if option != correct_answer:
            wrong_options.append(option)

    return random.choice(wrong_options)


# ------------------------------------------------------------
# Draw Current Question
# ------------------------------------------------------------
def draw_question():
    screen.fill(BACKGROUND_COLOR)

    title_text = title_font.render("AI Quiz Battle", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))

    player_text = score_font.render(
        f"Player Score: {player_score}",
        True,
        TEXT_COLOR
    )

    ai_text = score_font.render(
        f"AI Score: {ai_score}",
        True,
        TEXT_COLOR
    )

    screen.blit(player_text, (50, 100))
    screen.blit(ai_text, (650, 100))

    q = questions[current_question]

    question_text = question_font.render(
        q["question"],
        True,
        TEXT_COLOR
    )

    screen.blit(question_text, (80, 160))

    mouse_pos = pygame.mouse.get_pos()

    for i, button in enumerate(buttons):
        color = OPTION_COLORS[i]

        if button.collidepoint(mouse_pos):
            color = OPTION_HOVER_COLORS[i]

        pygame.draw.rect(screen, color, button, border_radius=12)

        option_label = chr(65 + i)  # A, B, C, D

        option_text = option_font.render(
            f"{option_label}. {q['options'][i]}",
            True,
            WHITE
        )

        screen.blit(option_text, (button.x + 20, button.y + 15))

    feedback = option_font.render(feedback_message, True, feedback_color)
    screen.blit(feedback, (80, 590))


# ------------------------------------------------------------
# Draw Final Screen
# ------------------------------------------------------------
def draw_game_over():
    screen.fill(BACKGROUND_COLOR)

    title = title_font.render(
        "Quiz Battle Finished!",
        True,
        TEXT_COLOR
    )

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    player_text = question_font.render(
        f"Player Score: {player_score}",
        True,
        TEXT_COLOR
    )

    ai_text = question_font.render(
        f"AI Score: {ai_score}",
        True,
        TEXT_COLOR
    )

    screen.blit(player_text, (320, 250))
    screen.blit(ai_text, (350, 320))

    if player_score > ai_score:
        winner = "You Win!"
        color = CORRECT_COLOR
    elif ai_score > player_score:
        winner = "AI Wins!"
        color = WRONG_COLOR
    else:
        winner = "It's a Tie!"
        color = TEXT_COLOR

    winner_text = title_font.render(winner, True, color)

    screen.blit(
        winner_text,
        (WIDTH // 2 - winner_text.get_width() // 2, 430)
    )


# ------------------------------------------------------------
# Main Game Loop
# ------------------------------------------------------------
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()

            for i, button in enumerate(buttons):
                if button.collidepoint(mouse_pos):

                    question = questions[current_question]
                    selected_answer = question["options"][i]
                    correct_answer = question["correct_answer"]

                    # Player answer
                    if selected_answer == correct_answer:
                        player_score += 1
                        feedback_message = "Correct! +1 point"
                        feedback_color = CORRECT_COLOR
                    else:
                        feedback_message = "Wrong answer!"
                        feedback_color = WRONG_COLOR

                    # AI answer
                    ai_choice = ai_answer(
                        correct_answer,
                        question["options"]
                    )

                    if ai_choice == correct_answer:
                        ai_score += 1

                    # Move to next question
                    current_question += 1

                    if current_question >= len(questions):
                        game_over = True

                    break

    if not game_over:
        draw_question()
    else:
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()