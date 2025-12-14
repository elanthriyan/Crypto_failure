Title: JWT algorithm confusion (RS256 -> HS256)
Difficulty: Hard
Time: 15-20 min

Description:
A service verifies JWT tokens using RS256 (RSA public key) but uses the public key as an HMAC secret if algorithm is HS256 due to mis-implementation.
Your task: forge a token with role=admin using the public key as HMAC key.

Files:
- jwt_service.py (verifies tokens)
- pubkey.pem (public key; included)
