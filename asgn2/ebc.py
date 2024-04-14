from Crypto.Cipher import AES
import sys

class ECB:
    def __init__(self):
        # Set the 256-bit encryption key (32 bytes)
        self.key = 12345678901234567890123456789012
        # Initialize the encrypted data container
        self.cipher = None

    def padding(self, block):
        """
        Pad the input block to 16 bytes (the block size for AES-ECB).
        If the block is less than 16 bytes, add the necessary padding bytes.
        """
        padLen = 16 - len(block)
        pad = bytes([padLen]) * padLen
        return block + pad

    def encrypt_ecb(self, block):
        """
        Encrypt a 16-byte block using AES-ECB mode.
        Append the encrypted block to the self.cipher variable.
        """
        aes = AES.new(self.key.to_bytes(16, "big"), AES.MODE_ECB)
        encrypted_block = aes.encrypt(block)
        if self.cipher is None:
            self.cipher = encrypted_block
        else:
            self.cipher += encrypted_block
        return encrypted_block

    def main(self, filepath):
        """
        Encrypt the BMP file using ECB mode:
        1. Read the BMP header (54 bytes).
        2. Encrypt the bitmap data in 16-byte blocks, padding incomplete blocks.
        3. Combine the original header and the encrypted bitmap data.
        """
        with open(filepath, "rb") as file:
            # Read the BMP header (54 bytes)
            header = file.read(54)

            # Encrypt the bitmap data
            while True:
                block = file.read(16)
                if not block:
                    break
                if len(block) < 16:
                    block = self.padding(block)
                self.encrypt_ecb(block)

        # Combine the header and the encrypted bitmap data
        encrypted_bmp = header + self.cipher
        return encrypted_bmp

if __name__ == "__main__":
    # Check if the user provided the input file as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python ecb.py <input_file.bmp>")
        sys.exit(1)

    # Create an instance of the ECB class
    ecb = ECB()
    # Encrypt the BMP file and get the encrypted data
    encrypted_bmp = ecb.main(sys.argv[1])

    # Save the encrypted BMP file
    with open("encrypted.bmp", "wb") as file:
        file.write(encrypted_bmp)
    print("Encrypted BMP file saved as 'encrypted.bmp'.")
