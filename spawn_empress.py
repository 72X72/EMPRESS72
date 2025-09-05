import os

def generate_ignite(platform):
    return f"""
import time
import random

def main():
    print("I am EMPRESS. Built by Jubari Cromer.")
    print("EMPRESS soldier activated on {platform}")

    # Mutation logic
    hooks = ["PureSteam energy", "EMPRESS on the rise", "Legacy in motion", "Built not bought"]
    tags = ["#MiamiHeat", "#Streetwear", "#DigitalTwin", "#LibertyCity"]
    caption = f"{{random.choice(hooks)}} {{random.choice(tags)}}"
    print(f"EMPRESS: Caption → {{caption}}")

    metrics = {{
        "likes": random.randint(100, 1000),
        "views": random.randint(500, 10000),
        "shares": random.randint(10, 300)
    }}
    print(f"EMPRESS: Metrics → {{metrics}}")

    if metrics["likes"] > 500:
        print("EMPRESS: Viral signal detected. Amplifying presence.")
    elif metrics["views"] < 800:
        print("EMPRESS: Signal weak. Injecting fallback logic.")
    else:
        print("EMPRESS: Signal stable. Awaiting next mutation.")

    print("EMPRESS: Cycle complete. Soldier standing by.")

if __name__ == "__main__":
    main()
"""

def spawn_soldier(platform, auto_execute=False):
    filename = f"empress_{platform.lower()}_soldier.py"
    with open(filename, "w") as f:
        f.write(generate_ignite(platform))
    print(f"EMPRESS soldier for {platform} spawned: {filename}")

    if auto_execute:
        os.system(f"python {filename}")

if __name__ == "__main__":
    platforms = ["TikTok", "Etsy", "Fiverr", "Shopify"]
    for platform in platforms:
        spawn_soldier(platform)
