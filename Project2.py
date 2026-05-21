import random

questions = {
    "easy": [
        {"question": "5 + 3 = ?", "answer": "8"},
        {"question": "10 - 4 = ?", "answer": "6"},
        {"question": "2 + 7 = ?", "answer": "9"}
    ],
    "medium": [
        {"question": "6 x 7 = ?", "answer": "42"},
        {"question": "15 + 18 = ?", "answer": "33"},
        {"question": "36 / 6 = ?", "answer": "6"}
    ],
    "hard": [
        {"question": "12 x 12 = ?", "answer": "144"},
        {"question": "25 x 8 = ?", "answer": "200"},
        {"question": "144 / 12 = ?", "answer": "12"}
    ]
}

levels = ["easy", "medium", "hard"]
level_index = 0
score = 0
num_questions = 10

print("Welcome to AI Quiz Master!")
print("Answer the questions and watch the quiz adapt.")

for i in range(num_questions):
    level = levels[level_index]
    q = random.choice(questions[level])

    print(f"\nQuestion {i+1} ({level.title()} Level)")
    print(q["question"])

    answer = input("Your answer: ").strip()

    if answer == q["answer"]:
        print("Correct!")
        score += 1

        if level_index < 2:
            level_index += 1
    else:
        print("Incorrect.")
        print("Correct answer:", q["answer"])

        if level_index > 0:
            level_index -= 1

print("\nQuiz Complete!")
print(f"Your score: {score}/{num_questions}")

if score == num_questions:
    print("Outstanding! Perfect score!")
elif score >= 8:
    print("Excellent work!")
elif score >= 5:
    print("Good job! Keep practicing.")
else:
    print("Keep practicing. You are improving!")