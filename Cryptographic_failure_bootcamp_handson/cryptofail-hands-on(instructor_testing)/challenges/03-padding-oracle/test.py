import requests

URL = "http://127.0.0.1:5050/check"

def oracle(ct):
    r = requests.post(URL, data=ct)
    return r.json()["valid"]

ct = open("ciphertext.bin", "rb").read()
iv = ct[:16]
body = ct[16:]

# Split blocks
blocks = [iv] + [body[i:i+16] for i in range(0, len(body), 16)]

def decrypt_block(block_index):
    prev_block = blocks[block_index-1]
    block = blocks[block_index]

    intermediate = [0]*16
    plaintext = [0]*16

    for pad in range(1, 17):
        for guess in range(256):
            attack = bytearray(prev_block)
            for i in range(1, pad):
                attack[-i] ^= intermediate[-i] ^ pad
            attack[-pad] ^= guess ^ pad
            attempt = bytes(attack) + block
            if oracle(attempt):
                intermediate[-pad] = guess
                plaintext[-pad] = guess ^ prev_block[-pad]
                break

    return bytes(plaintext)

# decrypt the last block
flag_block = decrypt_block(len(blocks)-1)
print(flag_block)
