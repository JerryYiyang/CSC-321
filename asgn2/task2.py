from Crypto.Cipher import AES
import os
import urllib.parse # for parsing URL

# Generate a random AES key and IV
key = os.urandom(16)
iv = os.urandom(16)

class ECB:
    def __init__(self):
        self.key = key

    def padding(self, block):
        pad_len = AES.block_size - len(block) % AES.block_size
        pad = bytes([pad_len]) * pad_len
        return block + pad

def submit(user_input):
    # Prepend and append the string
    input_string = f"userid=456;userdata={user_input};session-id=31337"

    # URL encode any ';' and '=' characters
    input_string = urllib.parse.quote(input_string, safe='')

    # Pad the string using PKCS#7
    ecb = ECB()
    padded_input = ecb.padding(input_string.encode())

    # Encrypt the padded string using AES-128-CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_input)

    return ciphertext

def verify(ciphertext):
    # Decrypt the ciphertext using AES-128-CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    
    # Unpad the decrypted plaintext
    unpadded_plaintext = plaintext[:-plaintext[-1]]
    
    # Check if the plaintext contains the ";admin=true;" pattern
    if b";admin=true;" in unpadded_plaintext:
        return True
    else:
        return False

# Example usage
ciphertext = submit("You're the man now, dog")
print("Ciphertext:", ciphertext.hex())
print("Verified:", verify(ciphertext))

# Demonstrate the bit-flipping attack
def manipulate_ciphertext(ciphertext):
    # Manipulate the ciphertext to flip a bit in the block
    # Assume we want to flip the first bit of the first block
    # This would flip the same bit in the second block due to CBC mode

    modified_ciphertext = bytearray(ciphertext)
    modified_ciphertext[0] ^= 1  # Flip the first bit of the first block

    return bytes(modified_ciphertext)

modified_ciphertext = manipulate_ciphertext(ciphertext)
print("Modified Ciphertext:", modified_ciphertext.hex())
print("Verified:", verify(modified_ciphertext))


