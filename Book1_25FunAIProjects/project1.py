import random

moves = ["rock", "paper", "scissors"]
player_history = []

def get_computer_move():
    if len(player_history) < 3:
        return random.choice(moves)

    most_common = max(set(player_history), key=player_history.count)

    if most_common == "rock":
        return "paper"
    elif most_common == "paper":
        return "scissors"
    else:
        return "rock"

def find_winner(player, computer):
    if player == computer:
        return "Tie!"

    if player == "rock" and computer == "scissors":
        return "You win!"
    elif player == "paper" and computer == "rock":
        return "You win!"
    elif player == "scissors" and computer == "paper":
        return "You win!"
    else:
        return "Computer wins!"

print("Welcome to Smart Rock-Paper-Scissors!")
print("Type rock, paper, or scissors.")
print("Type quit to stop the game.")

while True:
    player = input("\nYour move: ").lower()

    if player == "quit":
        break

    if player not in moves:
        print("Please type rock, paper, or scissors.")
        continue

    computer = get_computer_move()

    print("Computer chose:", computer)
    print(find_winner(player, computer))

    player_history.append(player)

print("\nGame over!")
print("Your move history:", player_history)
