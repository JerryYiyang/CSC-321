from Crypto.Cipher import AES
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
        
        # Remove padding
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]

        # Decode the URL-encoded string
        try:
            decrypted = urllib.parse.unquote(decrypted.decode('utf-8'))
        except UnicodeDecodeError:
            return False
        
        # Check if the decrypted ciphertext contains the ";admin=true;" pattern
        if ";admin=true;" in decrypted:
            return True
        else:
            return False

    def manipulate_ciphertext(self, ciphertext):
        block_size = AES.block_size
        
        # The desired plaintext pattern we want to achieve
        desired_plaintext = b";admin=true;"
        
        # Calculate the position in the plaintext where we want the pattern to appear
        prepend_length = len("userid=456;userdata=")
        position = prepend_length

        # Determine the block index and position within the block for the desired_plaintext
        block_index = position // block_size
        within_block_index = position % block_size

        # Create a mutable byte array of the ciphertext
        modified_ciphertext = bytearray(ciphertext)

        # Manipulate the bytes in the preceding block to achieve the desired plaintext
        for i in range(len(desired_plaintext)):
            block_pos = block_index * block_size + within_block_index + i
            prev_block_pos = block_pos - block_size
            modified_ciphertext[prev_block_pos] ^= desired_plaintext[i] ^ ciphertext[block_pos]

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
