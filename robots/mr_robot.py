import random

# Define the range of servers (1 to 100) and the fixed backdoor server
servers = [f"192.168.1.{i}" for i in range(1, 101)]
backdoor_server = "192.168.1.30"  # Fixed backdoor location

hints = [
    " fsociety is watching... Look closer at the numbers.",
    " It’s not random. Think like Elliot.",
    " Bro think properly, use your damn brain.",  
]

print("WELCOME TO FSOCIETY")
print("Evil Corp has 100 servers. One of them (192.168.1.30) has a backdoor.")
print("Your mission: Find the backdoor in 5 tries.\n")

tries = 5
hint_given = False

while tries > 0:
    print(f" Available servers: 192.168.1.1 to 192.168.1.100")
    guess = input("Enter the IP of the server you want to inspect: ").strip()

    if guess == backdoor_server:
        print("\n SUCCESS! You found the backdoor. fsociety welcomes you.")
        print(" FLAG: expX{The_b@3kDoor_i5_found}")
        break
    elif guess in servers:
        tries -= 1
        print(f" Wrong choice! {tries} tries left.")

        # Give a hint after 3 wrong guesses
        if tries == 2 and not hint_given:
            print("\n HINT:", random.choice(hints))
            hint_given = True
    else:
        print(" Invalid IP! Choose from 192.168.1.1 to 192.168.1.100.")

if tries == 0:
    print("\n GAME OVER! You failed. Better luck next time.")

print("\nGoodbye, hacker.")

# Flag: expX{The_b@3kDoor_i5_found}