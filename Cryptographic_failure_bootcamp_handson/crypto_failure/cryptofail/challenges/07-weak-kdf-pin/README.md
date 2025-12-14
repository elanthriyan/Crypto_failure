Title: Weak KDF with PIN (small space)
Difficulty: Medium-Hard
Time: 15-20 min

Description:
A service uses PBKDF2 with a zero salt and only 100 iterations to derive a key from a 4-digit PIN. The flag is encrypted using that key. Recover the PIN by brute force and get the flag.

Files:
- pin_checker.py (provides ciphertext and verifies PIN)
