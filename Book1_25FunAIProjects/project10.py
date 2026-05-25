print("Welcome to Math Tutor Bot!")
print("I will solve a problem and explain each step.\n")

num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))
operation = input("Choose +, -, *, or /: ")

if operation == "+":
    result = num1 + num2
    explanation = (
        f"To add {num1} and {num2}, "
        f"we combine the two numbers."
    )

elif operation == "-":
    result = num1 - num2
    explanation = (
        f"To subtract {num2} from {num1}, "
        f"we remove the second number from the first."
    )

elif operation == "*":
    result = num1 * num2
    explanation = (
        f"To multiply {num1} by {num2}, "
        f"we add {num1} a total of {num2} times."
    )

elif operation == "/":
    if num2 == 0:
        print("Division by zero is not allowed.")
        exit()
    result = num1 / num2
    explanation = (
        f"To divide {num1} by {num2}, "
        f"we determine how many times {num2} "
        f"fits into {num1}."
    )

else:
    print("Unknown operation.")
    exit()

print("\nStep-by-Step Explanation:")
print(explanation)

print("\nFinal Answer:")
print(f"{num1} {operation} {num2} = {result}")

if operation == "/" and result.is_integer():
    print(f"That means the quotient is {int(result)}.")
else:
    print("Great job! Keep practicing math every day.")
