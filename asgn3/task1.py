import hashlib
from Crypto.Cipher import AES # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore

# Define the IETF-suggested prime number and generator
q = int("B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371", 16)
alpha = int("A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5", 16)

print("Parameters:")
print("q:", q)
print("alpha:", alpha)
print()

# Generate private keys for Alice and Bob
private_key_A = 123456789  # Just an arbitrary value for demonstration
private_key_B = 987654321  # Just an arbitrary value for demonstration

print("Private keys:")
print("Alice:", private_key_A)
print("Bob:", private_key_B)
print()

# Calculate public keys for Alice and Bob
public_key_A = pow(alpha, private_key_A, q)
public_key_B = pow(alpha, private_key_B, q)

print("Public keys:")
print("Alice:", public_key_A)
print("Bob:", public_key_B)
print()

# Perform key exchange
shared_secret_A = pow(public_key_B, private_key_A, q)
shared_secret_B = pow(public_key_A, private_key_B, q)

# Convert shared secrets to bytes
shared_secret_A_bytes = shared_secret_A.to_bytes((shared_secret_A.bit_length() + 7) // 8, byteorder='big')
shared_secret_B_bytes = shared_secret_B.to_bytes((shared_secret_B.bit_length() + 7) // 8, byteorder='big')

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
