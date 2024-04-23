import hashlib
from Crypto.Cipher import AES # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore

# Define the prime number and generator for smaller parameters
q = 37
alpha = 5

print("Parameters:")
print("q:", q)
print("alpha:", alpha)
print()

# Generate private keys for Alice and Bob
private_key_A = 6  #arbitrary value for demonstration
private_key_B = 15   #arbitrary value for demonstration

print("Private keys:")
print("Alice:", private_key_A)
print("Bob:", private_key_B)
print()

# Calculate public keys for Alice and Bob
public_key_A = (alpha ** private_key_A) % q
public_key_B = (alpha ** private_key_B) % q

print("Public keys:")
print("Alice:", public_key_A)
print("Bob:", public_key_B)
print()

# Perform key exchange
shared_secret_A = (public_key_B ** private_key_A) % q
shared_secret_B = (public_key_A ** private_key_B) % q

# Convert shared secrets to bytes
shared_secret_A_bytes = shared_secret_A.to_bytes(32, byteorder='big')
shared_secret_B_bytes = shared_secret_B.to_bytes(32, byteorder='big')

# Hash the shared secrets using SHA256
k_A = hashlib.sha256(shared_secret_A_bytes).digest()[:16]
k_B = hashlib.sha256(shared_secret_B_bytes).digest()[:16]

print("Symmetric keys (truncated SHA256 hash of shared secrets):")
print("Alice:", k_A)
print("Bob:", k_B)
print()

# Define AES cipher
iv = b'16byteslongstrng'  # Corrected IV, should be 16 bytes long
cipher = AES.new(k_A, AES.MODE_CBC, iv=iv)

# Encrypt message from Alice to Bob
message_from_A = "Hi Bob!".encode()
ciphertext_A = cipher.encrypt(pad(message_from_A, AES.block_size))

# Decrypt message from Alice to Bob
cipher = AES.new(k_B, AES.MODE_CBC, iv=iv)
plaintext_B = unpad(cipher.decrypt(ciphertext_A), AES.block_size)

# Print the decrypted message
print("Decrypted message by Bob:", plaintext_B.decode())

