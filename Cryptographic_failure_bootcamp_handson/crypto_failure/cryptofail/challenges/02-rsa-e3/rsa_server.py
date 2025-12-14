#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
import math, json

FLAG = b"FLAG{rsa_low_e_cube_root_attack}"

# generate a small demo key (for the challenge we provide pubkey.pem and ciphertext)
key = RSA.generate(1024)
pub = key.publickey()
m = FLAG
m_int = bytes_to_long(m)
c = pow(m_int, 3, pub.n)  # e=3
open("pubkey.pem","wb").write(pub.export_key())
open("ciphertext.bin","wb").write(str(c).encode())
print("Created pubkey.pem and ciphertext.bin")
