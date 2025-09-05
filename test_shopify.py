import requests

STORE = os.getenv("SHOPIFY_ACCESS_TOKEN")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")  # your Admin API token

url = fos.getenv("SHOPIFY_ACCESS_TOKEN")
headers = {
    os.getenv("SHOPIFY_ACCESS_TOKEN"): TOKEN,
    os.getenv("SHOPIFY_ACCESS_TOKEN"): os.getenv("SHOPIFY_ACCESS_TOKEN")
}

r = requests.get(url, headers=headers)
print(os.getenv("SHOPIFY_ACCESS_TOKEN"), r.status_code)
print(os.getenv("SHOPIFY_ACCESS_TOKEN"), r.json())
