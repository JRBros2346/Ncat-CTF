import base64
import random
import string

def encrypt(message):
    # Step 1: Character shifting
    shifted = ""
    for i, char in enumerate(message):
        shifted += chr(ord(char) + i)

    # Step 2: Base64 encoding
    encoded = base64.b64encode(shifted.encode()).decode()

    # Step 3: Reversing
    reversed_encoded = encoded[::-1]

    # Step 4: XOR with a key
    key = 0xAA
    xor_encrypted = "".join([chr(ord(char) ^ key) for char in reversed_encoded])

    return xor_encrypted

original = ''.join(random.choices(string.ascii_uppercase, k=10))
encrypted = encrypt(original)
print(f"Encrypted message: {encrypted}")
guess = input("Guess: ").strip()
if guess == original:
    print("Correct guess!!")
    try:
        with open("flag") as f:
            flag = f.read().strip()
            print(f"The flag is: {flag}")
    except FileNotFoundError:
        print("Run in server for flag")
else:
    print("Wrong guess!!")
