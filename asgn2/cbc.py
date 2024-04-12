from Crypto.Cipher import AES # type: ignore

class CBC:
    def __init__(self):
        self.key = 12345678901234567890123456789012
        self.iv = 98765432109876543210987654321098
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
            self.iv = self.iv.to_bytes(16, "big")
            self.key = self.key.to_bytes(16, "big")
            while True:
                block = file.read(16)
                if not block:
                    break
                if len(block) < 16:
                    block = self.padding(block)
                self.encrypt(block)
        file.close()
        return self.cipher