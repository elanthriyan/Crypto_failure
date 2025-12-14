Title: OTP Key Reuse (Two-time pad)
Difficulty: Hard
Time: 15-20 min

Description:
Two messages were encrypted with the same one-time pad key (XOR). You are given two ciphertext files c1.bin and c2.bin.
One of the plaintexts contains the flag in ASCII like: FLAG{...}

Task:
Recover the flag from XORing the ciphertexts and analyzing the resulting output.

Files:
- server.py (simple file that generated the ciphertexts)
- ciphertexts/c1.bin
- ciphertexts/c2.bin
