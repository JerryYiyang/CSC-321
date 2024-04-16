# from Crypto.Cipher import AES


# # Generate a random AES key and IV
# key = os.urandom(16)
# iv = os.urandom(16)

# # class ECB:
# #     def __init__(self):
# #         self.key = key
# #         self.cipher = b""

# #     def padding(self, block):
# #         pad_len = 16 - len(block)
# #         pad = bytes([pad_len]) * pad_len
# #         return block + pad

# #     def encrypt(self, block):
# #         aes = AES.new(self.key, AES.MODE_ECB)
# #         encrypted_block = aes.encrypt(block)
# #         self.cipher += encrypted_block

# #     def decrypt(self, block):
# #         aes = AES.new(self.key, AES.MODE_ECB)
# #         decrypted_block = aes.decrypt(block)
# #         return decrypted_block

# def submit():

# def  verify():
# # (1) decrypt the string (you may use a AES-CBC decrypt library or implement your own CBC decrypt); 
# # (2) parse the string for the pattern “;admin=true;” and, 
# # (3) return true or false based on whether that string exists. If you’ve written submit() correctly, it should be impossible for a user to provide input to submit() that will result in verify() returning true.



import os
import urllib.parse
from Crypto.Cipher import AES

# Generate a random AES key and IV
key = os.urandom(16)
iv = os.urandom(16)

class ECB:
    def __init__(self):
        self.key = key

    def padding(self, block):
        pad_len = 16 - len(block)
        pad = bytes([pad_len]) * pad_len
        return block + pad

def submit(user_input):
    # Prepend and append the string
    input_string = f"userid=456;userdata={user_input};session-id=31337"

    # URL encode any ';' and '=' characters
    input_string = urllib.parse.quote(input_string, safe='')

    # Pad the string using PKCS#7 (from Task 1)
    ecb = ECB()
    padded_input = ecb.padding(input_string.encode())

    # Encrypt the padded string using AES-128-CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_input)

    return ciphertext

def verify(ciphertext):
    # Decrypt the ciphertext using AES-128-CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Check if the plaintext contains the ";admin=true;" pattern
    if b";admin=true;" in plaintext:
        return True
    else:
        return False

# Example usage
ciphertext = submit("You're the man now, dog")
print("Ciphertext:", ciphertext.hex())
print("Verified:", verify(ciphertext))

# Demonstrate the bit-flipping attack
# Hint: Flipping one bit in ciphertext block ci will result in a scrambled plaintext block mi, but will flip the same bit in plaintext block mi+1
modified_ciphertext = bytearray(ciphertext)
modified_ciphertext[16] ^= 0x01  # Flip a bit in the second ciphertext block
modified_ciphertext = bytes(modified_ciphertext)
print("Modified ciphertext:", modified_ciphertext.hex())
print("Verified (modified):", verify(modified_ciphertext))