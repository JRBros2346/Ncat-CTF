import os
import paramiko
import hashlib
import random
import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# --- Step 1: Simulate Flawed SSH Key Generation ---
def flawed_key_generation():
    """ Generates an RSA key pair with a flawed random number generator. """
    random.seed(42)  # Weak PRNG with fixed seed
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key

# --- Step 2: Save Public and Private Keys ---
def save_keys(private_key, partial=False):
    """ Saves the private key (full or partial) and public key """
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open("id_rsa.pub", "wb") as f:
        f.write(public_pem)
    
    if partial:
        partial_key = private_pem[:len(private_pem)//2]  # Save only half
        with open("id_rsa.partial", "wb") as f:
            f.write(partial_key)
    else:
        with open("id_rsa", "wb") as f:
            f.write(private_pem)

    return public_pem.decode()

# --- Step 3: Encrypt a Secret Token with AES ---
def encrypt_secret(private_key):
    """ Encrypts a secret message using a derived symmetric key. """
    secret_message = b"expX{cr@ck_th3_r&a_fl@g!}"
    
    derived_key = hashlib.sha256(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )).digest()[:16]  # Use first 16 bytes for AES key
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_message = secret_message + b" " * (16 - len(secret_message) % 16)  # PKCS#7 padding
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    
    with open("ciphertext.enc", "wb") as f:
        f.write(iv + ciphertext)  # Store IV + encrypted data

# --- Step 4: Simulated SSH Session Log ---
def generate_session_log():
    """ Creates a fake SSH session log containing hints. """
    log_content = """[SSH] Connecting to server...
[SSH] Key Exchange Method: RSA-OAEP (FLAWED)
[SSH] Authentication failed: Partial key detected
[SSH] Timing analysis suggests weak entropy in key gen
[SSH] Session terminated."""
    
    with open("session.log", "w") as f:
        f.write(log_content)
    
    return log_content

# --- Step 5: SSH Server ---
def handle_ssh_connection(client, addr, public_pem):
    """ Handles an SSH connection and sends challenge details. """
    print(f"[+] SSH Connection received from {addr}")
    session_log = generate_session_log()
    
    message = f"""
    Welcome to the SSH Challenge Server
    -----------------------------------
    {session_log}
    -----------------------------------
    Public Key:
    {public_pem}
    -----------------------------------
    Partial Private Key:
    {open("id_rsa.partial", "r").read()}
    -----------------------------------
    Can you reconstruct the key and decrypt the message?
    """
    client.send(message.encode())
    client.close()

def start_ssh_server(public_pem):
    """ Starts an SSH server to accept connections. """
    host_key = paramiko.RSAKey(filename="id_rsa")
    server = paramiko.ServerInterface()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 22))
    server_socket.listen(5)
    print("[+] SSH server started on port 22. Waiting for connections...")
    
    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_ssh_connection, args=(client, addr, public_pem)).start()

# --- Execution ---
private_key = flawed_key_generation()
public_pem = save_keys(private_key, partial=True)  # Save partial key
save_keys(private_key, partial=False)  # Save full key (hidden from user)
encrypt_secret(private_key)
start_ssh_server(public_pem)
