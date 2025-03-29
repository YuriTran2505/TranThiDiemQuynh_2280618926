from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Generate RSA key pair
server_key = RSA.generate(2048)

# List of connected clients (now thread-safe with a lock)
clients = []
clients_lock = threading.Lock()

# Function to encrypt message
def encrypt_message(key, message):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return iv + ciphertext

# Function to decrypt message
def decrypt_message(key, encrypted_message):
    if len(encrypted_message) < AES.block_size:
        raise ValueError("Message too short to contain IV")
    
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode('utf-8')

# Function to broadcast message to all clients except sender
def broadcast_message(sender_socket, message, sender_key):
    with clients_lock:
        for client, key in clients:
            if client != sender_socket:
                try:
                    encrypted = encrypt_message(key, message)
                    client.send(encrypted)
                except Exception as e:
                    print(f"Error sending to client: {e}")
                    clients.remove((client, key))
                    client.close()

# Function to handle client connection
def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")
    
    try:
        # Send server's public key to client
        client_socket.send(server_key.publickey().export_key(format='PEM'))

        # Receive client's public key
        client_public_key = RSA.import_key(client_socket.recv(2048))

        # Generate AES key for message encryption
        aes_key = get_random_bytes(16)  # AES-256

        # Encrypt the AES key using the client's public key
        cipher_rsa = PKCS1_OAEP.new(client_public_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.send(encrypted_aes_key)

        # Add client to the list
        with clients_lock:
            clients.append((client_socket, aes_key))

        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break  # Client disconnected

            try:
                decrypted_message = decrypt_message(aes_key, encrypted_message)
                print(f"Received from {client_address}: {decrypted_message}")

                if decrypted_message.lower() == "exit":
                    break

                # Broadcast to other clients
                broadcast_message(client_socket, decrypted_message, aes_key)
            except Exception as e:
                print(f"Error processing message from {client_address}: {e}")
                break

    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        # Clean up
        with clients_lock:
            if (client_socket, aes_key) in clients:
                clients.remove((client_socket, aes_key))
        client_socket.close()
        print(f"Connection with {client_address} closed")

# Accept and handle client connections
try:
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(
            target=handle_client, 
            args=(client_socket, client_address),
            daemon=True
        )
        client_thread.start()
except KeyboardInterrupt:
    print("Server shutting down...")
finally:
    server_socket.close()