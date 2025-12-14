from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
import gmpy2

pub = RSA.import_key(open("pubkey.pem").read())
c = int(open("ciphertext.bin").read())

# compute m = c^(1/3)
m, exact = gmpy2.iroot(c, 3)
print(long_to_bytes(int(m)))
