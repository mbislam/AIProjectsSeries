import random

mood = input(
    "Choose a mood (happy, spooky, mysterious, adventurous): "
).lower()

characters = [
    "a robot",
    "a dragon",
    "a detective",
    "a young wizard"
]

places = [
    "in a magical forest",
    "on Mars",
    "inside an ancient castle",
    "under the ocean"
]

events = [
    "found a secret map",
    "heard a strange sound",
    "discovered hidden treasure",
    "met a mysterious friend"
]

mood_descriptions = {
    "happy": "Everything felt bright and cheerful.",
    "spooky": "A cold wind whispered through the darkness.",
    "mysterious": "Something unusual was about to happen.",
    "adventurous": "The journey was full of excitement."
}

if mood not in mood_descriptions:
    print("Unknown mood. Using mysterious.")
    mood = "mysterious"

character = random.choice(characters)
place = random.choice(places)
event = random.choice(events)

story = (
    f"One day, {character} was {place}. "
    f"{mood_descriptions[mood]} "
    f"Suddenly, {character} {event}. "
    "The adventure changed everything."
)

print("\nYour AI-Generated Story:\n")
print(story)