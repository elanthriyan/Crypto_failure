#!/usr/bin/env python3
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import itertools, os, binascii

PIN = "0426"  # small 4-digit PIN (changeable)
salt = b'\x00'*8
key = PBKDF2(PIN, salt, dkLen=16, count=100)
FLAG = b"FLAG{weak_kdf_small_pin_bruteforce}"
cipher = AES.new(key, AES.MODE_ECB)
ct = cipher.encrypt(pad(FLAG, 16))
open("cipher.bin","wb").write(ct)
print("cipher.bin created")
