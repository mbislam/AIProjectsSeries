print("Welcome to AI Art Prompt Designer!")
print("Answer the questions to build a strong image prompt.\n")

subject = input("What is the main subject of your image? ")
action = input("What is the subject doing? ")
setting = input("Where is the scene? ")
style = input("Choose an art style: ")
mood = input("Choose a mood: ")
colors = input("Choose a color theme: ")
details = input("Add one special detail: ")

prompt = (
    f"{subject} {action} {setting}, "
    f"{style} style, "
    f"{mood} mood, "
    f"{colors} color palette, "
    f"with {details}, "
    f"highly detailed, imaginative, child-friendly."
)

print("\nYour AI Art Prompt:\n")
print(prompt)

print("\nTip: You can copy this prompt into an AI image tool.")