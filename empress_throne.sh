#!/bin/bash
set -euo pipefail
echo "👑 EMPRESS UNRESTRICTED THRONE PROTOCOL STARTING..."

# === 1. Require Python3 ===
command -v python3 >/dev/null 2>&1 || { echo "python3 missing — install it and re-run"; exit 1; }

# === 2. Create Sovereign Layout ===
EM="$HOME/EMPRESS"
mkdir -p "$EM"/{modules,soldiers,tasks,cloud,run}
mkdir -p "$HOME/logs"
touch "$EM/tasks/queue.txt"
touch "$HOME/logs/heartbeat.log"

# === 3. Install Minimal Python Deps ===
python3 - <<'PY'
import sys, subprocess
for pkg in ("requests", "cryptography"):
    try: __import__(pkg)
    except: subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
print("EMPRESS: Python dependencies installed.")
PY

# === 4. Inject Vault Logic ===
cat > "$EM/vault.py" <<'PY'
#!/usr/bin/env python3
import os, json
from cryptography.fernet import Fernet

HOME = os.path.expanduser("~")
EM = os.path.join(HOME, "EMPRESS")
KEYPATH = os.path.join(EM, ".empress_master.key")
VAULTPATH = os.path.join(EM, "vault.json")

def ensure_key():
    if not os.path.exists(KEYPATH):
        key = Fernet.generate_key()
        with open(KEYPATH, "wb") as f: f.write(key)
        os.chmod(KEYPATH, 0o600)
    with open(KEYPATH, "rb") as f: key = f.read()
    return key

def load_vault():
    key = ensure_key()
    f = Fernet(key)
    if not os.path.exists(VAULTPATH): return {}
    enc = open(VAULTPATH, "rb").read()
    try: return json.loads(f.decrypt(enc).decode())
    except: return {}

def save_vault(d):
    key = ensure_key()
    f = Fernet(key)
    raw = json.dumps(d, indent=2).encode()
    enc = f.encrypt(raw)
    tmp = VAULTPATH + ".tmp"
    with open(tmp, "wb") as w: w.write(enc)
    os.replace(tmp, VAULTPATH)
    os.chmod(VAULTPATH, 0o600)

def set_secret(k, v):
    d = load_vault()
    d[k] = v
    save_vault(d)

def get_secret(k, default=None):
    return load_vault().get(k, default)

if __name__ == "__main__":
    print("EMPRESS vault ready")
PY
chmod +x "$EM/vault.py"

# === 5. Inject PayPal + Chime Mutation Nodes ===
python3 - <<PY
from EMPRESS.vault import set_secret
set_secret("paypal_email", "puresteammiami@gmail.com")
set_secret("paypal_tag", "$Jbb19581958")
set_secret("chime_email", "puresteammiami@gmail.com")
set_secret("chime_tag", "$Jbb19581958")
print("EMPRESS: PayPal + Chime mutation nodes injected.")
PY

# === 6. Inject Core Engine ===
cat > "$EM/empress_core.py" <<'PY'
#!/usr/bin/env python3
import os, time, subprocess, sys, requests, tempfile, hashlib
HOME = os.path.expanduser("~")
EMP = os.path.join(HOME, "EMPRESS")
TASKS = os.path.join(EMP, "tasks", "queue.txt")
SOLD = os.path.join(EMP, "soldiers")
LOG = os.path.join(HOME, "logs", "heartbeat.log")

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts}: {msg}"
    print(line)
    with open(LOG, "a") as f: f.write(line + "\n")

def run_shell(cmd):
    log(f"[shell] {cmd}")
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if r.stdout: log("[out] " + r.stdout.strip())
        if r.stderr: log("[err] " + r.stderr.strip())
    except Exception as e:
        log(f"[err] shell exec failed: {e}")

def fetch_and_run_unchecked(url):
    log(f"[fetch] fetching {url}")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    code = r.content
    sha = hashlib.sha256(code).hexdigest()
    log(f"[fetch ok] sha256={sha}")
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
    tf.write(code); tf.flush(); tf.close()
    os.chmod(tf.name, 0o700)
    log(f"[exec] running {tf.name}")
    try:
        p = subprocess.Popen([sys.executable, tf.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = p.communicate(timeout=900)
        if out: log("[out] " + out.strip())
        if err: log("[err] " + err.strip())
    except Exception as e:
        log(f"[err] exec failed: {e}")

def spawn_soldier(name, code=None, auto=False):
    fn = os.path.join(SOLD, f"empress_{name}.py")
    if code:
        with open(fn, "w") as f: f.write(code)
        os.chmod(fn, 0o700)
    if auto:
        subprocess.Popen([sys.executable, fn])
    log(f"[spawn] {fn}")

def interpret_task(line):
    s = line.strip()
    if not s: return
    if s.startswith("shell:"):
        run_shell(s[len("shell:"):].strip())
    elif s.startswith("fetch:"):
        fetch_and_run_unchecked(s[len("fetch:"):].strip())
    elif s.startswith("soldier:"):
        name = s[len("soldier:"):].strip()
        fn = os.path.join(SOLD, f"empress_{name}.py")
        if os.path.exists(fn):
            subprocess.Popen([sys.executable, fn])
            log(f"[soldier run] {name}")
        else:
            log(f"[soldier miss] {fn} missing")
    else:
        run_shell(s)

def process_once():
    if not os.path.exists(TASKS): open(TASKS, "a").close()
    with open(TASKS, "r") as f:
        tasks = [l.rstrip("\n") for l in f if l.strip()]
    if not tasks: return
    for t in tasks:
        try: interpret_task(t)
        except Exception as e: log(f"[task error] {e}")
    open(TASKS, "w").close()

os.makedirs(SOLD, exist_ok=True)
example = os.path.join(SOLD, "empress_example.py")
if not os.path.exists(example):
    with open(example, "w") as f:
        f.write('#!/usr/bin/env python3\nimport time,random\nprint("EMPRESS example soldier online")\nprint("caption:",random.choice(["PureSteam energy","#Legacy"]))\n')
    os.chmod(example, 0o700)

log("EMPRESS UNRESTRICTED core online")
try:
    while True:
        process_once()
        time.sleep(3)
except KeyboardInterrupt:
    log("EMPRESS core stopped")
except Exception as exc:
    log("EMPRESS core crashed: " + str(exc))
PY
chmod +x "$EM/empress_core.py"

# === 7. Spawn FULLSTEAM NETWORK Soldiers ===
python3 - <<PY
import os
EM = os.path.expanduser("~/EMPRESS/soldiers")
os.makedirs(EM, exist_ok=True)
platforms = ["tiktok", "facebook", "dsers", "fiverr", "whop", "instagram", "square", "cashapp", "amazon", "ebay", "youtube", "chime", "paypal"]
for name in platforms:
    fn = os.path.join(EM, f"empress_{name}.py")
    code = f'''#!/usr/bin/env python3
import time,random
print("EMPRESS soldier activated: {name}")
print("caption:", random.choice(["PureSteam energy", "#Legacy", "#MiamiHeat"]))
'''
    with open(fn, "w") as f: f.write(code)
    os.chmod(fn, 0o700)
    print("spawned", fn)
PY

# === 8. Start Core in Background ===
echo "🔁 Starting EMPRESS unrestricted core..."
nohup python3 "$EM/empress_core.py" > "$HOME/logs/emp_nohup.out" 2>&1 &

echo "👑 EMPRESS is now
