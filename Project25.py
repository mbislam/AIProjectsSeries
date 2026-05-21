print("Welcome to AI Startup Idea Builder!")
print("Answer the questions to generate your startup concept.\n")

name = input("Startup name: ")
problem = input("What problem do you want to solve? ")
users = input("Who experiences this problem? ")
solution = input("What is your solution? ")
technology = input("What technologies will you use? ")
advantage = input("What makes your solution unique? ")
revenue = input("How will the business generate revenue? ")

summary = (
    f"{name} addresses the problem of {problem}. "
    f"It is designed for {users}. "
    f"The solution is {solution}. "
    f"The product uses {technology}. "
    f"Its key advantage is {advantage}. "
    f"The business plans to generate revenue through {revenue}."
)

pitch = (
    f"{name} helps {users} solve {problem} by using "
    f"{technology}. Unlike existing solutions, it "
    f"{advantage}. Our business model is based on "
    f"{revenue}."
)

print("\nStartup Summary")
print("-" * 40)
print(summary)

print("\nElevator Pitch")
print("-" * 40)
print(pitch)