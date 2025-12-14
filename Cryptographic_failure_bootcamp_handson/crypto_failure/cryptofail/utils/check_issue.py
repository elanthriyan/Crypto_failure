import os
import json
import re
import hashlib

# Map challenge folder name → GitHub Secret name
FLAG_MAP = {
    "01-otp-reuse": "FLAG_01_OTP_REUSE",
    "02-rsa-e3": "FLAG_02_RSA_E3",
    "03-padding-oracle": "FLAG_03_PADDING_ORACLE",
    "04-aes-ecb-cutpaste": "FLAG_04_ECB",
    "05-jwt-alg-confusion": "FLAG_05_JWT",
    "06-lcg-token-predict": "FLAG_06_LCG",
    "07-weak-kdf-pin": "FLAG_07_KDF",
}

# Load GitHub event payload
event_path = os.environ.get("GITHUB_EVENT_PATH")
if not event_path:
    print("No GitHub event payload found")
    exit(0)

with open(event_path, "r") as f:
    event = json.load(f)

issue = event.get("issue", {})
body = issue.get("body", "")
user = issue.get("user", {}).get("login", "unknown")

# Extract Challenge and Flag from issue body
challenge_match = re.search(r"Challenge:\s*(.+)", body)
flag_match = re.search(r"Flag:\s*(FLAG\{.*?\})", body)

if not challenge_match or not flag_match:
    print("Invalid issue format (Challenge/Flag missing)")
    exit(0)

challenge = challenge_match.group(1).strip()
flag = flag_match.group(1).strip()

if challenge not in FLAG_MAP:
    print(f"Unknown challenge: {challenge}")
    exit(0)

# Get expected hash from GitHub Secrets
secret_name = FLAG_MAP[challenge]
expected_hash = os.environ.get(secret_name)

if not expected_hash:
    print(f"Missing GitHub secret: {secret_name}")
    exit(1)

# Hash submitted flag
submitted_hash = hashlib.sha256(flag.encode()).hexdigest()

if submitted_hash != expected_hash:
    print("Invalid flag submitted")
    exit(0)

print(f"Valid flag submitted by {user} for {challenge}")

# ---------------- LEADERBOARD UPDATE ----------------

leaderboard_json_path = "leaderboard.json"
leaderboard_md_path = "leaderboard.md"

# Load leaderboard.json
if os.path.exists(leaderboard_json_path):
    with open(leaderboard_json_path, "r") as f:
        leaderboard = json.load(f)
else:
    leaderboard = {}

# Ensure one row per participant
leaderboard.setdefault(user, [])
if challenge not in leaderboard[user]:
    leaderboard[user].append(challenge)

# Save leaderboard.json
with open(leaderboard_json_path, "w") as f:
    json.dump(leaderboard, f, indent=2)

# Generate leaderboard.md (ONE ROW PER PARTICIPANT)
with open(leaderboard_md_path, "w") as f:
    f.write("# 🏆 Leaderboard\n\n")
    f.write("| Participant | Challenges Solved |\n")
    f.write("|------------|------------------|\n")

    for participant in sorted(leaderboard.keys()):
        solved = ", ".join(sorted(leaderboard[participant]))
        f.write(f"| {participant} | {solved} |\n")

print("Leaderboard updated successfully")
