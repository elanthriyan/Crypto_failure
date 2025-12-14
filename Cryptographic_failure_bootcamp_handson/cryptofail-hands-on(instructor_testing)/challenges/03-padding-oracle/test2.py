import requests
from Crypto.Util.Padding import unpad

URL = "http://127.0.0.1:5000/check"
BLOCK_SIZE = 16


def oracle(ciphertext: bytes) -> bool:
    r = requests.post(URL, data=ciphertext)
    return r.status_code == 200


def split_blocks(data, size=16):
    return [data[i:i+size] for i in range(0, len(data), size)]


def decrypt_block(prev_block, curr_block):
    recovered = bytearray(BLOCK_SIZE)
    intermediate = bytearray(BLOCK_SIZE)

    for pad in range(1, BLOCK_SIZE + 1):
        found = False

        for guess in range(256):
            attack = bytearray(prev_block)

            # Fix known bytes to match current padding
            for i in range(1, pad):
                attack[-i] ^= intermediate[-i] ^ pad

            # Apply guess
            attack[-pad] ^= guess ^ pad

            if oracle(bytes(attack + curr_block)):
                # Avoid false positive when pad == 1
                if pad == 1 and guess == prev_block[-pad]:
                    continue

                intermediate[-pad] = guess
                recovered[-pad] = guess ^ prev_block[-pad]
                found = True
                break

        if not found:
            raise Exception(f"Failed to decrypt byte with pad={pad}")

    return bytes(recovered)


def main():
    with open("ciphertext.bin", "rb") as f:
        ciphertext = f.read()

    blocks = split_blocks(ciphertext)

    plaintext = b""
    for i in range(1, len(blocks)):
        pt_block = decrypt_block(blocks[i - 1], blocks[i])
        plaintext += pt_block

    # Remove PKCS#7 padding
    plaintext = unpad(plaintext, BLOCK_SIZE)

    print("\nRecovered plaintext:")
    print(plaintext.decode())


if __name__ == "__main__":
    main()
