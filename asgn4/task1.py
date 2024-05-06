import hashlib
import random

def hash_input(input_str):
    input_bytes = input_str.encode('utf-8')
    sha256_hash = hashlib.sha256(input_bytes)
    hash_hex = sha256_hash.hexdigest()
    return hash_hex[:6]

print("input 1")
print(hash_input("00000000"))
print(hash_input("00000001"))
print("input 2")
print(hash_input("00000010"))
print(hash_input("00000011"))

truncated = {}

while True:
    input_str = str(random.getrandbits(64))  # Generate a random input string
    truncated_digest = hash_input(input_str)
    if truncated_digest in truncated:
        print("Collision found!")
        print(f"Input 1: {truncated[truncated_digest]}")
        print(f"Input 2: {input_str}")
        print(f"Truncated Digest (Hexadecimal): {truncated_digest}\n")
        break
    else:
        truncated[truncated_digest] = input_str