from Crypto.Cipher import AES
import os
import sys

class ECB:
    def __init__(self, filename):
        self.key = os.urandom(16)  # Generate a random 128-bit key
        self.cipher = b""  # Initialize ciphertext
        self.filename = filename

    def padding(self, block):
        pad_len = 16 - len(block)
        pad = bytes([pad_len]) * pad_len
        return block + pad

    def encrypt(self, block):
        aes = AES.new(self.key, AES.MODE_ECB)
        encrypted_block = aes.encrypt(block)
        self.cipher += encrypted_block

    def main(self):
        with open(self.filename, "rb") as file:
            # Read and preserve BMP header
            bmp_header = file.read(54)
            self.cipher += bmp_header  # Append header to ciphertext
            while True:
                block = file.read(16)
                if not block:  # End of file
                    break
                if len(block) < 16:
                    block = self.padding(block)
                self.encrypt(block)
        return self.cipher

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ecb.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    ecb_cipher = ECB(filename)
    encrypted_data = ecb_cipher.main()
    with open("encrypted.bmp", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

