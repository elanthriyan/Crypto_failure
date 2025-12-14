# jwt_service.py
# Fixed to support the "vulnerable" HS256 path that uses the public key bytes as HMAC secret.

import json
import re
import base64
from jose import jwt

# Load public key PEM file
with open("pubkey.pem", "rb") as f:
    pem_bytes = f.read()

# PUB_PEM: text version (for RS256 verification)
PUB_PEM = pem_bytes.decode()

# PUB_DER: raw DER bytes (for treating as HMAC secret in HS256 path)
# Remove PEM headers/footers and base64-decode
pem_text = PUB_PEM
pem_body = re.sub(r"-----.*?-----", "", pem_text, flags=re.S).strip()
PUB_DER = base64.b64decode(pem_body)

FLAG = "FLAG{jwt_alg_confusion_allows_hmac_signing}"

def verify(token):
    """
    Verify token. Returns payload dict on success; returns FLAG when role=admin;
    returns None on failure.
    """
    try:
        # decode header to inspect alg
        header_b64 = token.split(".")[0]
        header_json = base64.urlsafe_b64decode(header_b64 + "===").decode()
        header = json.loads(header_json)
    except Exception:
        # Malformed token
        return None

    alg = header.get("alg")

    try:
        if alg == "RS256":
            # Verify using RSA public key (PEM)
            payload = jwt.decode(token, PUB_PEM, algorithms=["RS256"])
            # return flag if admin
            if payload.get("role") == "admin":
                return FLAG
            return payload

        if alg == "HS256":
            # Vulnerable path: uses public key DER bytes as HMAC secret
            # (this is the intentional vulnerability for the challenge)
            payload = jwt.decode(token, PUB_DER, algorithms=["HS256"])
            if payload.get("role") == "admin":
                return FLAG
            return payload

    except Exception:
        return None

# Demo: if you run this module directly it will do nothing.
if __name__ == "__main__":
    print("jwt_service ready")
