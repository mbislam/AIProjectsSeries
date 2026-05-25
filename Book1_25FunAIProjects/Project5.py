pet_name = input("What do you want to name your pet? ")

hunger = 5
energy = 5
happiness = 5

print("\nWelcome to Virtual Pet Assistant!")
print("Commands: feed, play, sleep, status, quit")

def show_status():
    print("\nPet Status")
    print("Name:", pet_name)
    print("Hunger:", hunger)
    print("Energy:", energy)
    print("Happiness:", happiness)

while True:
    command = input("\nWhat do you want to do? ").lower()

    if command == "feed":
        hunger -= 2
        happiness += 1
        print(pet_name, "enjoyed the food!")

    elif command == "play":
        happiness += 2
        energy -= 2
        hunger += 1
        print(pet_name, "had fun playing!")

    elif command == "sleep":
        energy += 3
        hunger += 1
        print(pet_name, "took a nap.")

    elif command == "status":
        show_status()

    elif command == "quit":
        print("Goodbye from", pet_name + "!")
        break

    else:
        print("I do not understand that command.")

    hunger = max(0, min(10, hunger))
    energy = max(0, min(10, energy))
    happiness = max(0, min(10, happiness))

    if hunger >= 8:
        print(pet_name, "is very hungry!")
    if energy <= 2:
        print(pet_name, "is very tired!")
    if happiness <= 2:
        print(pet_name, "feels lonely.")