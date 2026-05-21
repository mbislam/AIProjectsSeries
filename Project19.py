print("Welcome to Study Planner AI!")
print("This program will create a study plan for you.\n")

subjects = []

num_subjects = int(
    input("How many subjects do you need to study? ")
)

for i in range(num_subjects):
    print(f"\nSubject {i + 1}")

    name = input("Subject name: ")

    difficulty = int(
        input("Difficulty from 1 to 5: ")
    )

    if difficulty < 1:
        difficulty = 1
    elif difficulty > 5:
        difficulty = 5

    subjects.append({
        "name": name,
        "difficulty": difficulty
    })

total_time = int(
    input("\nTotal study time in minutes: ")
)

total_difficulty = sum(
    subject["difficulty"] for subject in subjects
)

print("\nYour Personalized Study Plan")
print("-" * 35)

for subject in subjects:
    recommended_time = (
        subject["difficulty"] / total_difficulty
    ) * total_time

    print(
        f"{subject['name']}: "
        f"{recommended_time:.0f} minutes"
    )

print("-" * 35)
print("Tip: Take a 5-minute break after every 25 minutes.")