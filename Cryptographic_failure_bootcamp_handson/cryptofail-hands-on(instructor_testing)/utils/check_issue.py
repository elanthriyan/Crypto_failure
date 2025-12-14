#!/usr/bin/env python3
import os, sys, json, hashlib, requests, datetime

GITHUB_API = "https://api.github.com"
REPO = os.environ.get("GITHUB_REPOSITORY")
if not REPO:
    print("GITHUB_REPOSITORY not found (are you running locally?). Exiting.")
    sys.exit(1)

# load flag hashes map:
flag_hashes = {}
secret_json = os.environ.get("FLAG_HASHES_JSON")
if secret_json:
    flag_hashes = json.loads(secret_json)
else:
    local = ".github/flags.json"
    if os.path.exists(local):
        flag_hashes = json.load(open(local))
    else:
        print("No flags provided in FLAG_HASHES_JSON or .github/flags.json. Exiting.")
        sys.exit(1)

# GitHub context
event_path = os.environ.get("GITHUB_EVENT_PATH", "/github/workflow/event.json")
if not os.path.exists(event_path):
    print("GITHUB_EVENT_PATH not present:", event_path)
    sys.exit(1)
event = json.load(open(event_path))
issue = event.get("issue")
if not issue:
    print("No issue in event payload")
    sys.exit(1)

issue_number = issue["number"]
issue_body = issue.get("body","")
issue_user = issue["user"]["login"]

token = os.environ.get("GITHUB_TOKEN")
if not token:
    print("GITHUB_TOKEN missing")
    sys.exit(1)

headers = {"Authorization": f"token {token}", "Accept":"application/vnd.github+json"}

def sha256_hex(s):
    return hashlib.sha256(s.encode()).hexdigest()

# check for any of the flags
found = None
found_challenge = None
for cid, h in flag_hashes.items():
    # We'll search for a pattern FLAG{...} or the exact flag; user should provide the flag in the issue body
    # We only have the hash, so we check each word that looks like a flag and compare hashes
    # Extract candidate tokens
    words = [w.strip() for w in issue_body.split() if len(w) >= 6 and len(w) <= 200]
    for w in words:
        if sha256_hex(w) == h:
            found = w
            found_challenge = cid
            break
    if found:
        break

def post_comment(msg):
    url = f"{GITHUB_API}/repos/{REPO}/issues/{issue_number}/comments"
    resp = requests.post(url, headers=headers, json={"body": msg})
    return resp

def add_label(label):
    url = f"{GITHUB_API}/repos/{REPO}/issues/{issue_number}/labels"
    return requests.post(url, headers=headers, json={"labels":[label]})

def update_leaderboard(user, challenge):
    path = "leaderboard.json"
    data = {}
    if os.path.exists(path):
        data = json.load(open(path))
    # ensure user entry exists
    if user not in data:
        data[user] = {"solved":[], "score":0}
    if challenge in data[user]["solved"]:
        return False
    data[user]["solved"].append(challenge)
    data[user]["score"] = len(data[user]["solved"])
    # save file and commit via API
    # get file sha if exists
    repo_url = f"{GITHUB_API}/repos/{REPO}/contents/{path}"
    get_resp = requests.get(repo_url, headers=headers)
    if get_resp.status_code == 200:
        sha = get_resp.json()["sha"]
    else:
        sha = None
    content = json.dumps(data, indent=2)
    import base64
    payload = {
        "message": f"Leaderboard update: {user} solved {challenge}",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": os.environ.get("GITHUB_REF", "main").split("/")[-1]
    }
    if sha:
        payload["sha"] = sha
    put_resp = requests.put(repo_url, headers=headers, json=payload)
    return put_resp.status_code in (200,201)

# Main logic
if not found:
    post_comment("Thanks for your submission — we couldn't find a valid flag in your issue. Please include the flag string (e.g. `FLAG{...}`) in the issue body.")
    sys.exit(0)

# valid flag found
post_comment(f"✅ Valid flag for **{found_challenge}** confirmed. Good job @{issue_user}!\n\nFlag: `{found}`")
add_label("solved")
updated = update_leaderboard(issue_user, found_challenge)
if updated:
    post_comment(f"Leaderboard updated. @{issue_user} now has a new solved challenge: **{found_challenge}**")
else:
    post_comment(f"@{issue_user} already had **{found_challenge}** solved; no leaderboard change.")
