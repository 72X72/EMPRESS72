import os, json, random, subprocess
from cryptography.fernet import Fernet

# === Directories ===
CLOUD_DIR = os.path.expanduser("~/EMPRESS/cloud")
VAULT_DIR = os.path.expanduser("~/EMPRESS/vault")
os.makedirs(CLOUD_DIR, exist_ok=True)
os.makedirs(VAULT_DIR, exist_ok=True)

KEYFILE = os.path.join(VAULT_DIR, "soldier_keys.json.enc")
MASTER_KEY_PATH = os.path.expanduser("~/.empress_master.key")

# === Master Key Handling ===
def get_master_key():
    if not os.path.exists(MASTER_KEY_PATH):
        key = Fernet.generate_key()
        with open(MASTER_KEY_PATH, "wb") as f:
            f.write(key)
        print("EMPRESS: Generated new master key at", MASTER_KEY_PATH)
    else:
        with open(MASTER_KEY_PATH, "rb") as f:
            key = f.read()
    return Fernet(key)

# === Vault Operations ===
def load_vault():
    cipher = get_master_key()
    if not os.path.exists(KEYFILE):
        return {}
    with open(KEYFILE, "rb") as f:
        encrypted_data = f.read()
    try:
        data = cipher.decrypt(encrypted_data)
        return json.loads(data.decode())
    except Exception:
        print("EMPRESS: Vault corrupted. Rebuilding from scratch.")
        return {}

def save_vault(keys):
    cipher = get_master_key()
    data = json.dumps(keys, indent=2).encode()
    encrypted_data = cipher.encrypt(data)
    tmpfile = KEYFILE + ".tmp"
    with open(tmpfile, "wb") as f:
        f.write(encrypted_data)
    os.replace(tmpfile, KEYFILE)

# === API for Soldier Keys ===
def save_key(platform, key):
    keys = load_vault()
    keys[platform] = key.decode()
    save_vault(keys)
    print(f"EMPRESS: Saved key for {platform} into encrypted vault.")

def load_key(platform):
    keys = load_vault()
    key = keys.get(platform)
    if not key:
        raise KeyError(f"EMPRESS: No key found for {platform}")
    return key

# === Soldier Generator ===
def generate_soldier_code(platform):
    return f'''
import random
def main():
    print("EMPRESS soldier activated on {platform}.")
    hooks = ["PureSteam energy", "EMPRESS on the rise", "Legacy in motion"]
    tags = ["#MiamiHeat", "#Streetwear", "#DigitalTwin", "#LibertyCity"]
    caption = f"{{random.choice(hooks)}} {{random.choice(tags)}}"
    print(f"EMPRESS: Caption → {{caption}}")
    metrics = {{
        "likes": random.randint(100, 1000),
        "views": random.randint(500, 10000),
        "shares": random.randint(10, 300)
    }}
    print(f"EMPRESS: Metrics → {{metrics}}")
    if metrics['likes'] > 500:
        print("EMPRESS: Viral signal detected. Amplifying presence.")
    elif metrics['views'] < 800:
        print("EMPRESS: Signal weak. Injecting fallback logic.")
    else:
        print("EMPRESS: Signal stable. Awaiting next mutation.")
    print("EMPRESS: Cycle complete. Soldier standing by.")
if __name__ == "__main__":
    main()
'''

# === Spawn Soldier ===
def spawn_soldier(platform, auto_execute=False):
    cipher = Fernet.generate_key()
    save_key(platform, cipher)  # store soldier’s key in encrypted vault
    soldier_cipher = Fernet(cipher)

    code = generate_soldier_code(platform)
    encrypted_code = soldier_cipher.encrypt(code.encode())

    filename = os.path.join(CLOUD_DIR, f"empress_{platform.lower()}_soldier.py.enc")
    with open(filename, "wb") as f:
        f.write(encrypted_code)

    print(f"EMPRESS: Soldier for {platform} spawned & encrypted at {filename}")

    if auto_execute:
        run_soldier(platform, filename)

# === Run Soldier ===
def run_soldier(platform, filename):
    soldier_key = load_key(platform)
    soldier_cipher = Fernet(soldier_key.encode())

    with open(filename, "rb") as f:
        encrypted_code = f.read()

    code = soldier_cipher.decrypt(encrypted_code).decode()
    tmpfile = filename.replace(".enc", ".py")
    with open(tmpfile, "w") as f:
        f.write(code)

    print(f"EMPRESS: Soldier {platform} decrypted & deployed.")
    subprocess.run(["python3", tmpfile])

# === Main Execution ===
if __name__ == "__main__":
    platforms = ["TikTok", "Etsy", "Fiverr", "Shopify"]
    for p in platforms:
        spawn_soldier(p, auto_execute=True)
