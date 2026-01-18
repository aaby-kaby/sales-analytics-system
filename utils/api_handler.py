import requests

def fetch_product_category(product_id):
    try:
        response = requests.get(f"https://dummyjson.com/products/{product_id[-1]}")
        data = response.json()
        return data.get("category", "Unknown")
    except:
        return "Unknown"