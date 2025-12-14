Title: CBC Padding Oracle
Difficulty: Hard
Time: 20 min

Description:
A web endpoint returns whether provided ciphertext decrypts to valid PKCS7 padding (simulated). Use the oracle to decrypt the last block and recover the last block which contains the flag.

Files:
- oracle_server.py (Flask app providing /check endpoint)
