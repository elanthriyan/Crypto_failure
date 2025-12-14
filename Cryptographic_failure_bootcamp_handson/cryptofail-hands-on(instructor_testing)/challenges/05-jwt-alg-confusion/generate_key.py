from Crypto.PublicKey import RSA

# Generate a 2048-bit RSA key pair
key = RSA.generate(2048)

# Export public key
pubkey = key.publickey().export_key()

with open("pubkey.pem", "wb") as f:
    f.write(pubkey)

print("pubkey.pem generated successfully!")
