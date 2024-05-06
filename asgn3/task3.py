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

# If Mallory sends 1 as c', then she will know what s is since 1 powered by anything is 1
# then mod by anything is also 1 so s will be 1.

# Also, just in general, if Mallory sends a c', then Bob will recieved modified plaintext m' because of c' and the
# message will be manipulated and cause confusion

# Sign(m3, d) = m3^d mod n = (m1 * m2)^d mod n = (m1^d * m2^d) mod n