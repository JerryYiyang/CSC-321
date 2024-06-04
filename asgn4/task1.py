import hashlib
import random
import time

# Function to hash input and truncate the digest
def hash_input(input_str, digest_size):
    input_bytes = input_str.encode('utf-8')
    sha256_hash = hashlib.sha256(input_bytes)
    hash_hex = sha256_hash.hexdigest()
    # Truncate the hash to the specified digest size in bits
    truncated_digest = hash_hex[:digest_size // 4]
    return truncated_digest

# Function to find collision for a specific digest size
def find_collision(digest_size):
    truncated = {}
    inputs = 0
    start_time = time.time()

    while True:
        input_length = random.randint(10, 50)  # Ensure reasonable string lengths
        input_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=input_length))
        truncated_digest = hash_input(input_str, digest_size)
        inputs += 1
        if truncated_digest in truncated:
            end_time = time.time()
            collision_time = end_time - start_time
            return inputs, collision_time
        else:
            truncated[truncated_digest] = input_str

# Digest sizes to test (in bits)
digest_sizes = list(range(8, 52, 2))

# Variables to store results
results = []

# Measure inputs and time for each digest size
for digest_size in digest_sizes:
    print(f"Testing digest size: {digest_size} bits")
    inputs, collision_time = find_collision(digest_size)
    results.append((digest_size, inputs, collision_time))

# Print results for Excel
print("Digest Size (bits)\tNumber of Inputs\tCollision Time (seconds)")
for result in results:
    print(f"{result[0]}\t{result[1]}\t{result[2]}")
