c1 = open("ciphertexts/c1.bin","rb").read()
c2 = open("ciphertexts/c2.bin","rb").read()

x = bytes(a ^ b for a, b in zip(c1, c2))

print(x)
