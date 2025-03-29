from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_secret(private_key, server_public_key):
    shared_key = private_key.exchange(server_public_key)
    return shared_key

def main():
    # Load server's public key
    with open("server_public_key.pem", "rb") as f:
        server_public_key = serialization.load_pem_public_key(
            f.read(),
            backend=None  # Default backend is automatically selected
        )
    
    # Get parameters from server's public key
    parameters = server_public_key.parameters()
    
    # Generate client's key pair
    private_key, public_key = generate_client_key_pair(parameters)
    
    # Save client's public key (optional)
    with open("client_public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    # Derive shared secret
    shared_secret = derive_shared_secret(private_key, server_public_key)
    
    # Print the shared secret in hex format
    print("Shared Secret:", shared_secret.hex())

if __name__ == "__main__":
    main()