import random

print("Welcome to AI Story Writer!")

character = input("Choose a character: ")
setting = input("Choose a setting: ")
theme = input("Choose a theme: ")

openings = [
    "One day,",
    "Long ago,",
    "In a distant world,",
    "On a magical morning,",
    "Many years from now,"
]

events = [
    "discovered a hidden secret",
    "met an unexpected friend",
    "faced a difficult challenge",
    "found a mysterious object",
    "learned a powerful lesson"
]

endings = [
    "Everything changed forever.",
    "The adventure became legendary.",
    "A new friendship began.",
    "The mystery was finally solved.",
    "The hero returned home wiser than before."
]

opening = random.choice(openings)
event = random.choice(events)
ending = random.choice(endings)

story = (
    f"{opening} {character} was {setting}. "
    f"There, {character} {event}. "
    f"The experience taught an important lesson about {theme}. "
    f"{ending}"
)

print("\nYour AI-Generated Story:\n")
print(story)