Title: RSA low exponent (e=3)
Difficulty: Hard
Time: 15-20 min

Description:
A message (the flag) was encrypted using RSA with very small public exponent e=3 and no padding. The ciphertext is available and the public key is provided.
Because the message was small enough, it can be recovered by taking the integer cube root of ciphertext.

Files:
- rsa_server.py (shows how ciphertext was made)
- pubkey.pem (public key)
