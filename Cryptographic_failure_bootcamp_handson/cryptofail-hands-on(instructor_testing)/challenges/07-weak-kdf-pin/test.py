from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

ct = open("cipher.bin", "rb").read()

for pin in range(10000):
    PIN = f"{pin:04d}"
    key = PBKDF2(PIN, b'\x00'*8, dkLen=16, count=100)
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        pt = unpad(cipher.decrypt(ct), 16)
        if b"FLAG" in pt:
            print("PIN:", PIN)
            print("FLAG:", pt.decode())
            break
    except:
        pass
