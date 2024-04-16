from Crypto.Cipher import AES # type: ignore
import os
import urllib.parse # for parsing URL

class Main:
    def __init__(self):
        self.key = os.urandom(16)
        self.iv = os.urandom(16)

    #edited cbc code
    def padding(self, block):
        pad_len = AES.block_size - len(block) % AES.block_size
        pad = bytes([pad_len]) * pad_len
        return block + pad
    #edited cbc code
    def encrypt(self, block):
        xor = bytes(x ^ y for x, y in zip(self.iv, block))
        return AES.new(self.key, AES.MODE_ECB).encrypt(xor)

    def submit(self, user_input):
        # Prepend and append the string
        input_string = f"userid=456;userdata={user_input};session-id=31337"

        # URL encode any ';' and '=' characters
        input_string = urllib.parse.quote(input_string, safe='')

        # Pad the string using PKCS#7
        padded_input = self.padding(input_string.encode())

        # Encrypt the padded string using AES-128-CBC
        ciphertext = self.encrypt(padded_input)

        return ciphertext
    
    def verify(self, ciphertext):
        # Decrypt the ciphertext using AES-128-CBC
        decrypted = AES.new(self.key, AES.MODE_CBC).decrypt(ciphertext)
        plaintext = bytes(x ^ y for x, y in zip(self.iv, decrypted))
        
        # Unpad the decrypted plaintext
        unpadded_plaintext = plaintext[:-plaintext[-1]]
        
        # Check if the plaintext contains the ";admin=true;" pattern
        if b";admin=true;" in unpadded_plaintext:
            return True
        else:
            return False
        
    # Demonstrate the bit-flipping attack
    def manipulate_ciphertext(self, ciphertext):
        # Manipulate the ciphertext to flip a bit in the block
        # Assume we want to flip the first bit of the first block
        # This would flip the same bit in the second block due to CBC mode

        modified_ciphertext = bytearray(ciphertext)
        modified_ciphertext[0] ^= 1  # Flip the first bit of the first block

        return bytes(modified_ciphertext)