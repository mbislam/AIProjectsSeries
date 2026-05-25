import random

characters = [
    "a clumsy robot",
    "a superhero cat",
    "a sleepy wizard",
    "a curious alien",
    "a detective penguin"
]

settings = [
    "at a pizza shop",
    "on the Moon",
    "inside a haunted school",
    "in a secret laboratory",
    "at the beach"
]

problems = [
    "drops all the pizzas",
    "loses the secret map",
    "accidentally turns invisible",
    "presses the wrong button",
    "wakes up a giant monster"
]

endings = [
    "builds a flying pizza drone",
    "saves the day accidentally",
    "makes everyone laugh",
    "finds a clever solution",
    "becomes the town hero"
]

character = random.choice(characters)
setting = random.choice(settings)
problem = random.choice(problems)
ending = random.choice(endings)

print("Your Comic Strip Idea:\n")
print(f"Character: {character}")
print(f"Setting: {setting}")
print(f"Problem: {problem}")
print(f"Ending: {ending}")

print("\nStory Summary:")
print(
    f"{character} is {setting}. "
    f"One day, {character} {problem}. "
    f"In the end, {character} {ending}."
)