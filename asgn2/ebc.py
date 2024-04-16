from Crypto.Cipher import AES
import os

class ECB:
    def __init__(self):
        self.key = os.urandom(16)  # Generate a random 128-bit key
        self.cipher = b""  # Initialize ciphertext

    def padding(self, block):
        pad_len = 16 - len(block)
        pad = bytes([pad_len]) * pad_len
        return block + pad

    def encrypt(self, block):
        aes = AES.new(self.key, AES.MODE_ECB)
        encrypted_block = aes.encrypt(block)
        self.cipher += encrypted_block

    def main(self, filename):
        with open(filename, "rb") as file:
            while True:
                block = file.read(16)
                if not block:
                    break
                if len(block) < 16:
                    block = self.padding(block)
                self.encrypt(block)
        return self.cipher
