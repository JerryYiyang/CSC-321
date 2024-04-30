from Crypto.Util import number
import math

class RSA:
    def __init__(self):
        self.e = 65537
        # bit size inside the .getPrime() can be changed
        self.p = number.getPrime(1024)
        self.q = number.getPrime(1024)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.d = self.calc_d(self.e, self.phi)

    def get_n(self):
        return self.n

    def encrypt(self, m):
        return pow(m, self.e, self.n)

    def decrypt(self, c):
        return pow(c, self.d, self.n)
        
    def extended_gcd(self, a, b):
        if b == 0:
            return a, 1, 0
        else:
            gcd, x, y = self.extended_gcd(b, a % b)
            return gcd, y, x - (a // b) * y

    def calc_d(self, e, phi):
        gcd, x, y = self.extended_gcd(e, phi)
        return x % phi

