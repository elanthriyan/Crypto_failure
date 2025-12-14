from hashlib import sha256

A = 1103515245
C = 12345
M = 2**31

tokens = open("tokens.txt").read().splitlines()

def token_from_state(s):
    return sha256((str(s)+"static_secret_salt").encode()).hexdigest()[:32]

# brute force for seed
for seed in range(2**20): # small range only for demo
    s = seed
    ok = True
    for t in tokens:
        s = (A*s + C) % M
        if token_from_state(s) != t:
            ok = False
            break
    if ok:
        print("found seed:", seed)
        break
