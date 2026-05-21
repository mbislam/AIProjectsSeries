print("Think of a secret number between 1 and 100.")
print("I will try to guess it!")

low = 1
high = 100
guess_count = 0

while True:
    guess = (low + high) // 2
    guess_count += 1

    print(f"\nMy guess is: {guess}")
    feedback = input(
        "Enter h (too high), l (too low), or c (correct): "
    ).lower()

    if feedback == "c":
        print(f"I guessed your number in {guess_count} guesses!")
        break
    elif feedback == "h":
        high = guess - 1
    elif feedback == "l":
        low = guess + 1
    else:
        print("Please enter h, l, or c.")