#!/usr/bin/env python3
import os
from Crypto.Random import get_random_bytes
import binascii

FLAG = "FLAG{otp_key_reuse_xor_breaks_secrecy}"
m1 = b"This is a secret message. " + FLAG.encode() + b" End."
m2 = b"Another innocent message with some predictable text. End."

# pad to same length
L = max(len(m1), len(m2))
m1 = m1.ljust(L, b' ')
m2 = m2.ljust(L, b' ')

key = get_random_bytes(L)  # reused key (vuln)
c1 = bytes(a ^ b for a,b in zip(m1, key))
c2 = bytes(a ^ b for a,b in zip(m2, key))
os.makedirs("ciphertexts", exist_ok=True)
open("ciphertexts/c1.bin","wb").write(c1)
open("ciphertexts/c2.bin","wb").write(c2)
print("Generated ciphertexts/c1.bin and c2.bin")
