import hashlib
from Crypto.Cipher import AES # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore

# part 1
# Define the prime number and generator for smaller parameters
def mitm1():
    q = 37
    alpha = 5

    # Generate private keys for Alice and Bob
    private_key_A = 6  #arbitrary value for demonstration
    private_key_B = 15   #arbitrary value for demonstration

    # No need to calculate public keys since they're getting replaced anyway

    # Perform key exchange using q instead of public keys
    # Both results are just 0
    shared_secret_A = (q ** private_key_A) % q
    shared_secret_B = (q ** private_key_B) % q

    shared_secret_A_bytes = shared_secret_A.to_bytes(32, byteorder='big')
    shared_secret_B_bytes = shared_secret_B.to_bytes(32, byteorder='big')

    k_A = hashlib.sha256(shared_secret_A_bytes).digest()[:16]
    k_B = hashlib.sha256(shared_secret_B_bytes).digest()[:16]

    # Define AES cipher
    iv = b'16byteslongstrng'
    cipher = AES.new(k_A, AES.MODE_CBC, iv=iv)

    # Encrypt message from Alice to Bob
    message_from_A = "Hi Bob!".encode()
    print("Alice's message: 'Hi Bob!'")
    ciphertext_A = cipher.encrypt(pad(message_from_A, AES.block_size))

    # Now, Mallory works to decode ciphertext_A
    temp = 0
    mallory_s_B_bytes = temp.to_bytes(32, byteorder='big')
    mallory_k_B = hashlib.sha256(mallory_s_B_bytes).digest()[:16]
    cipher = AES.new(mallory_k_B, AES.MODE_CBC, iv=iv)
    plaintext_B = unpad(cipher.decrypt(ciphertext_A), AES.block_size)
    print(plaintext_B)

    # Repeat to decode Bob's message to Alice

# part 2

def mitm2():
    # Define the prime number and generator for smaller parameters
    q = 37
    alpha = 1

    print("Parameters:")
    print("q:", q)
    print("alpha:", alpha)
    print()

    # Generate private keys for Alice and Bob
    private_key_A = 6  #arbitrary value for demonstration
    private_key_B = 15   #arbitrary value for demonstration

    # Calculate public keys for Alice and Bob
    public_key_A = (alpha ** private_key_A) % q
    public_key_B = (alpha ** private_key_B) % q

    # Since alpha is one the resulting public key is just 1

    print("Public keys:")
    print("Alice:", public_key_A)

    # Perform key exchange
    shared_secret_A = (public_key_B ** private_key_A) % q
    shared_secret_B = (public_key_A ** private_key_B) % q

    # the resulting shared secret is also 1

    # Convert shared secrets to bytes
    shared_secret_A_bytes = shared_secret_A.to_bytes(32, byteorder='big')
    shared_secret_B_bytes = shared_secret_B.to_bytes(32, byteorder='big')

    # Hash the shared secrets using SHA256
    k_A = hashlib.sha256(shared_secret_A_bytes).digest()[:16]
    k_B = hashlib.sha256(shared_secret_B_bytes).digest()[:16]

    # Define AES cipher
    iv = b'16byteslongstrng'  # Corrected IV, should be 16 bytes long
    cipher = AES.new(k_A, AES.MODE_CBC, iv=iv)

    # Encrypt message from Alice to Bob
    message_from_A = "Hi Bob!".encode()
    print("Alice's message: 'Hi Bob!'")
    ciphertext_A = cipher.encrypt(pad(message_from_A, AES.block_size))

    temp = 1
    mallory_s_B_bytes = temp.to_bytes(32, byteorder='big')
    mallory_k_B = hashlib.sha256(mallory_s_B_bytes).digest()[:16]
    cipher = AES.new(mallory_k_B, AES.MODE_CBC, iv=iv)
    plaintext_B = unpad(cipher.decrypt(ciphertext_A), AES.block_size)
    print(plaintext_B)

    # Now repeat to get Bob's message

if __name__ == "__main__":
    mitm2()