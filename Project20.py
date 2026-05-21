print("Welcome to Personal Bio Generator!")
print("Answer a few questions, and I will create a short bio.\n")

name = input("What is your name? ")
role = input("What is your role or grade level? ")
interests = input("What are your interests? ")
skills = input("What skills are you proud of? ")
goal = input("What is one goal or dream you have? ")

tone = input(
    "Choose a tone: friendly, professional, or creative: "
).lower()

if tone == "professional":
    bio = (
        f"{name} is a {role} with strong interests in {interests}. "
        f"{name} is developing skills in {skills} and is working toward "
        f"the goal of {goal}."
    )

elif tone == "creative":
    bio = (
        f"Meet {name}, a curious {role} who loves exploring {interests}. "
        f"With growing talents in {skills}, {name} is on a journey to "
        f"{goal} and make creative ideas come alive."
    )

else:
    bio = (
        f"Hi! My name is {name}. I am a {role}, and I enjoy {interests}. "
        f"I am proud of my skills in {skills}. One of my goals is to "
        f"{goal}."
    )

print("\nYour Personal Bio:\n")
print(bio)