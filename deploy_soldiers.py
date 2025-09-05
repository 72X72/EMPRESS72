import subprocess
from spawn_empress import spawn_empress

config = {
    "daily_target": 1000,
    "platform_hooks": ["post", "track", "remix"],
    "narration": True
}

platforms = ["TikTok", "Etsy", "Fiverr", "Shopify"]

for platform in platforms:
    path = spawn_empress(platform, config)
    subprocess.run(["python3", f"{path}/ignite.py"])
    print(f"EMPRESS: {platform} soldier deployed from {path}")
