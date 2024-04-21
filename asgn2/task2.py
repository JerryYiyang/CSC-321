from Crypto.Cipher import AES # type: ignore
import os
import urllib.parse

class Main:
    def __init__(self):
        self.key = os.urandom(16)
        self.iv = os.urandom(16)

    def padding(self, block):
        pad_len = AES.block_size - len(block) % AES.block_size
        pad = bytes([pad_len]) * pad_len
        return block + pad

    def encrypt(self, block):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(block)

    def submit(self, user_input):
        # Prepend and append the string
        input_string = f"userid=456;userdata={user_input};session-id=31337;admin=true;"
        
        # URL encode any ';' and '=' characters
        input_string = urllib.parse.quote(input_string, safe='')
       
        # Pad the string using PKCS#7
        padded_input = self.padding(input_string.encode())
        # Encrypt the padded string using AES-128-CBC
        ciphertext = self.encrypt(padded_input)
        return ciphertext

    def verify(self, ciphertext):
        # Decrypt the ciphertext using AES-128-CBC
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = cipher.decrypt(ciphertext)
        
        # Decode the URL-encoded string
        decrypted = urllib.parse.unquote(decrypted.decode())
        
        # Check if the decrypted ciphertext contains the ";admin=true;" pattern
        if ";admin=true;" in decrypted:
            return True
        else:
            return False

    def manipulate_ciphertext(self, ciphertext):
        # Decrypt the ciphertext to find the position of ";admin=true;"
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = cipher.decrypt(ciphertext)

        # Check if the ";admin=true;" pattern is present anywhere in the decrypted ciphertext
        if b";admin=true;" in decrypted:
            print(".")
        else:
            print(".")
            return ciphertext

        # Calculate the block index based on the pattern index
        block_size = AES.block_size
        pattern_index = decrypted.find(b";admin=true;")
        block_index = pattern_index // block_size
        offset = block_index * block_size

        # Flip the last bit of the block containing the ";admin=true;" pattern
        modified_ciphertext = bytearray(ciphertext)
        modified_ciphertext[offset - 1] ^= 0x01  # Flipping the last bit of the previous block
        modified_ciphertext[offset + AES.block_size - 1] ^= 0x01  # Flipping the corresponding bit in the next block

        # Adjust the padding to ensure valid padding after the bit-flipping operation
        padding_length = 16 - (len(decrypted) % block_size)
        modified_ciphertext = modified_ciphertext[:-padding_length] + bytes([padding_length]) * padding_length

        return bytes(modified_ciphertext)

# Instantiate the Main class
main = Main()

# Submit user input and verify ciphertext
user_input = "You're the man now, dog"
ciphertext = main.submit(user_input)
print("Ciphertext:", ciphertext)
verification_result = main.verify(ciphertext)
print("Verification Result:", verification_result)

# Manipulate the ciphertext and verify again
manipulated_ciphertext = main.manipulate_ciphertext(ciphertext)
print("\nManipulated Ciphertext:", manipulated_ciphertext)
manipulated_verification_result = main.verify(manipulated_ciphertext)
print("Manipulated Verification Result:", manipulated_verification_result)
