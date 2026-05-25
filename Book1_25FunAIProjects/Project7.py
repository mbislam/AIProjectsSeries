flashcards = {
    "Python": "A programming language.",
    "Variable": "A container for storing data.",
    "Loop": "A way to repeat code.",
    "Function": "A reusable block of code.",
    "List": "A collection of items.",
    "Dictionary": "A collection of key-value pairs.",
    "AI": "Technology that helps computers perform intelligent tasks.",
    "Algorithm": "A step-by-step method for solving a problem."
}

print("Welcome to Flashcard Generator!")
print("Press Enter to reveal each answer.\n")

for term, definition in flashcards.items():
    print("Question:", term)
    input("Press Enter to see the answer...")
    print("Answer:", definition)
    print("-" * 40)

print("Great job! You reviewed all flashcards.")