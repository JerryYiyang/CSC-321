from Crypto.Cipher import AES # type: ignore
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


class CBC:
    def __init__(self):
        self.key = os.urandom(16)
        self.iv = os.urandom(16)
        self.cipher = None

    def padding(self, block):
        padLen = 16 - len(block)
        # creates padLen number of bytes needed
        pad = bytes([padLen]) * padLen
        return block + pad
    
    # takes in 128 bit block of plain text at a time
    def encrypt(self, block):
        xor = bytes(x ^ y for x, y in zip(self.iv, block))
        temp = AES.new(self.key, AES.MODE_ECB).encrypt(xor)
        if self.cipher == None:
            self.cipher = temp
        else:
            self.cipher += temp
            self.iv = temp

    def main(self, filepath):
        with open(filepath, "rb") as file:
            while True:
                block = file.read(16)
                if not block:
                    break
                if len(block) < 16:
                    block = self.padding(block)
                self.encrypt(block)
        file.close()
        return self.cipher