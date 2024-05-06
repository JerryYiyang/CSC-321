import hashlib

def hash_input(input_str):
    input_bytes = input_str.encode('utf-8')
    sha256_hash = hashlib.sha256(input_bytes)
    return sha256_hash.hexdigest()

print(hash_input("00000000"))
print(hash_input("00000001"))
