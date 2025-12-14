Title: AES-ECB Cut-and-Paste — forge admin
Difficulty: Medium-Hard
Time: 15-20 min

Description:
A naive "bank" web app creates user profiles (email, uid, role) and encrypts them using AES-ECB with a secret key.
Your goal is to craft a ciphertext that, when decrypted by the server, gives role=admin (flag shows only to admin).

Files:
- bank_demo.py (server that encrypts/decrypts profiles)
