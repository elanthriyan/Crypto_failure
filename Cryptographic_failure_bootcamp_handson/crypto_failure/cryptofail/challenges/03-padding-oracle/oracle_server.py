#!/usr/bin/env python3
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import binascii

app = Flask(__name__)
KEY = b"ThisIsA16ByteKey"

FLAG = b"FLAG{cbc_padding_oracle_revealed_last_block}"
pt = b"A" * 16 + FLAG  # flag in the last block
cipher = AES.new(KEY, AES.MODE_CBC)
ct = cipher.iv + cipher.encrypt(pad(pt, 16))
open("ciphertext.bin","wb").write(ct)

@app.route("/check", methods=["POST"])
def check():
    data = request.get_data()
    try:
        iv = data[:16]
        body = data[16:]
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        dec = cipher.decrypt(body)
        unpad(dec, 16)
        return jsonify({"valid": True})
    except Exception:
        return jsonify({"valid": False})

if __name__ == "__main__":
    print("ciphertext.bin created; run this as a challenge server.")
    app.run(host="0.0.0.0", port=5050)
