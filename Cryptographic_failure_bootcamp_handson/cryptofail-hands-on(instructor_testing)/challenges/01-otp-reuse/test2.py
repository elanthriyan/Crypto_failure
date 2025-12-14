x = b'\x15\x06\x06\x07H\x0c\x01\x00\x08N\x1d\n\x00\x17\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0eW/8)g\x08\x00\x19\x15\x7f\x1b\x17\x1c;\x1b\x06\x01\x12\x073\x1dO\x06:\x1a\x06KA.\x1d;]ECRECY]\x00eND\x0e'

print("".join(chr(b) if 32 <= b <= 126 else "." for b in x))

xor_bytes = x
crib = b"SECRECY"

# find where ECRECY appears
idx = xor_bytes.find(b"ECRECY")
print("Index:", idx)

key_fragment = bytes([xor_bytes[idx + i] ^ crib[i] for i in range(len(crib))])
print("Recovered key fragment:", key_fragment)


with open("ciphertexts/c2.bin", "rb") as f:
    c1 = f.read()

plaintext = bytes([c1[i] ^ key_fragment[i % len(key_fragment)] for i in range(len(c1))])
print(plaintext)
