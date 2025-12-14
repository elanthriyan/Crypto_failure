#!/usr/bin/env python3
import time, struct, base64
from hashlib import sha256

# LCG parameters (intentionally weak)
A = 1103515245
C = 12345
M = 2**31

def lcg_next(x):
    return (A * x + C) % M

def token_from_state(s):
    # token is hex of sha256(state||secret)[0:16]
    return sha256((str(s) + "static_secret_salt").encode()).hexdigest()[:32]

# emulate issuance
seed = int(time.time()) & 0xffffffff
s = seed
tokens = []
for i in range(4):
    s = lcg_next(s)
    tokens.append(token_from_state(s))

open("tokens.txt","w").write("\n".join(tokens))
FLAG = "FLAG{lcg_predictability_gives_tokens}"
open("flag.txt","w").write(FLAG)
print("tokens.txt created")
