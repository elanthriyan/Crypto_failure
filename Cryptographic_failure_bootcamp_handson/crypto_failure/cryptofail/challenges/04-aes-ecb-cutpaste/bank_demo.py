#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

KEY = b"YELLOW SUBMARINE"  # 16 bytes

def profile_for(email):
    email = email.replace("&","").replace("=","")
    profile = f"email={email}&uid=10&role=user"
    return profile.encode()

def encrypt_profile(profile):
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(pad(profile,16))

def decrypt_and_get_role(ct):
    cipher = AES.new(KEY, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ct),16).decode()
    # if role=admin, print the flag
    if "role=admin" in pt:
        return "FLAG{ecb_cut_and_paste_admin_created}"
    return pt

if __name__ == "__main__":
    # sample usage: generate a block with 'admin' padded
    p = profile_for("foo@bar.com")
    ct = encrypt_profile(p)
    open("cipher.bin","wb").write(ct)
    print("Wrote cipher.bin; craft a new cipher by cutting/pasting blocks to get role=admin.")
