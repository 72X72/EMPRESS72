#!/usr/bin/env python3
import json, requests, datetime, time

# -------------------------------
# LOAD CONFIG
# -------------------------------
with open("config.json") as f:
    c = json.load(f)

SHOPIFY_URL = f"https://{c['shopify_key']}:{c['shopify_secret']}@{c['shop']}.myshopify.com/admin/api/2025-07/products.json"
HEADERS = {"X-Shopify-Access-Token": c['shopify_token']}

# -------------------------------
# TIKTOK TREND SCORING
# -------------------------------
TREND_HASHTAGS = ["#TikTokMadeMeBuyIt", "#viralproducts"]

def fetch_tiktok_trends():
    """ Placeholder for real TikTok trends """
    return {
        "Wireless Earbuds": 95,
        "LED Strip Lights": 92,
        "Phone Stand": 90,
        "Cool Mug": 88,
        "Mini Projector": 85
    }

# -------------------------------
# SHOPIFY FUNCTIONS
# -------------------------------
def fetch_shopify_products():
    r = requests.get(SHOPIFY_URL, headers=HEADERS)
    if r.status_code != 200:
        print(f"[{datetime.datetime.now()}] Shopify fetch error: {r.status_code}, {r.text}")
        return []
    return r.json().get("products", [])

def score_products(products):
    trends = fetch_tiktok_trends()
    scored = []
    for p in products:
        title = p.get("title", "")
        score = trends.get(title, 50)  # default 50 if not trending
        scored.append({"product": p, "score": score})
    return sorted(scored, key=lambda x: x["score"], reverse=True)

def auto_publish(products):
    for item in products[:5]:  # publish top 5 trending
        p = item["product"]
        print(f"[{datetime.datetime.now()}] Publishing: {p['title']} (${p['variants'][0]['price']}) - Score: {item['score']}")
        # Optional: add Shopify API calls or social draft posts here

# -------------------------------
# MAIN LOOP
# -------------------------------
def main_loop(poll_interval=3600):
    while True:
        print(f"\n=== EMPRESS cycle started at {datetime.datetime.now()} ===")
        products = fetch_shopify_products()
        print(f"[{datetime.datetime.now()}] Fetched {len(products)} products from Shopify")
        if products:
            scored = score_products(products)
            auto_publish(scored)
        else:
            print(f"[{datetime.datetime.now()}] No products found from suppliers yet.")
        print(f"=== EMPRESS cycle complete at {datetime.datetime.now()} ===\n")
        time.sleep(poll_interval)

if __name__ == "__main__":
    main_loop(poll_interval=3600)  # run every 1 hour
