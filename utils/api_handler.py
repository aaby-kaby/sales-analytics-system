import requests

def fetch_product_category(product_id):
    try:
        response = requests.get(f"https://dummyjson.com/products/{product_id[-1]}")
        data = response.json()
        return data.get("category", "Unknown")
    except:
        return "Unknown"
    




# utils/api_handler.py

BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()
        data = response.json()
        print("API fetch successful")
        return data.get("products", [])
    except Exception as e:
        print("API fetch failed:", e)
        return []
    

#create product mapping
def create_product_mapping(api_products):
    """
    Creates mapping of product ID to product info
    """
    mapping = {}

    for product in api_products:
        mapping[product["id"]] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
        }

    return mapping



#Enrich Transactions with API Data
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product info
    """
    enriched = []

    for t in transactions:
        enriched_txn = t.copy()

        try:
            # Extract numeric ID: P101 -> 101
            product_id_num = int("".join(filter(str.isdigit, t["ProductID"])))

            if product_id_num in product_mapping:
                api_data = product_mapping[product_id_num]
                enriched_txn["API_Category"] = api_data["category"]
                enriched_txn["API_Brand"] = api_data["brand"]
                enriched_txn["API_Rating"] = api_data["rating"]
                enriched_txn["API_Match"] = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None
                enriched_txn["API_Match"] = False

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched.append(enriched_txn)

    return enriched




#Save Enriched Data to File
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get(h, "")) if t.get(h) is not None else ""
                for h in headers
            ]
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")