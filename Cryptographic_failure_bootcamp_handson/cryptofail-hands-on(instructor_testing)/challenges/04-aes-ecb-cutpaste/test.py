# exploit_direct.py — direct encryption of the admin profile (for testing)
from bank_demo import encrypt_profile, decrypt_and_get_role

# Directly build the profile string you want (this bypasses profile_for/email limitations)
profile = "email=test@example.com&uid=10&role=admin".encode()

# Encrypt the profile bytes
cipher = encrypt_profile(profile)

# Send the ciphertext to the decrypt function (server-side behavior)
res = decrypt_and_get_role(cipher)
print("Result:", res)
