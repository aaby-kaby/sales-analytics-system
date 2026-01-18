def clean_sales_data(raw_records):
    valid_records = []
    invalid_count = 0

    for record in raw_records:
        parts = record.split("|")

        if len(parts) != 8:
            invalid_count += 1
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        if not tid.startswith("T"):
            invalid_count += 1
            continue

        if not cid or not region:
            invalid_count += 1
            continue

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except:
            invalid_count += 1
            continue

        if qty <= 0 or price < 0:
            invalid_count += 1
            continue

        pname = pname.replace(",", "")

        valid_records.append({
            "TransactionID": tid,
            "Date": date,
            "ProductID": pid,
            "ProductName": pname,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cid,
            "Region": region
        })

    print(f"Total records parsed: {len(raw_records)}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records


def parse_transactions(raw_lines):
    """
    Parses raw sales lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        pname = pname.replace(",", "")

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except ValueError:
            continue

        transactions.append({
            "TransactionID": tid,
            "Date": date,
            "ProductID": pid,
            "ProductName": pname,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cid,
            "Region": region
        })

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Q2 Task 1.3
    Validates and filters transactions
    Returns (valid_transactions, invalid_count, summary)
    """
    valid_transactions = []
    invalid_count = 0
    valid_amounts = []

    # Collect valid transaction amounts and regions
    valid_regions = set()

    for t in transactions:
        if (
            t["TransactionID"].startswith("T") and
            t["ProductID"].startswith("P") and
            t["CustomerID"].startswith("C") and
            t["Quantity"] > 0 and
            t["UnitPrice"] > 0 and
            t["Region"]
        ):
            amount = t["Quantity"] * t["UnitPrice"]
            valid_amounts.append(amount)
            valid_regions.add(t["Region"])
        else:
            invalid_count += 1

    # Display valid regions and amount range
    print("Available Regions:", valid_regions)

    if valid_amounts:
        print("Transaction Amount Range:", min(valid_amounts), "-", max(valid_amounts))
    else:
        print("Transaction Amount Range: No valid data")

    # Apply filters
    for t in transactions:
        if not (
            t["TransactionID"].startswith("T") and
            t["ProductID"].startswith("P") and
            t["CustomerID"].startswith("C") and
            t["Quantity"] > 0 and
            t["UnitPrice"] > 0 and
            t["Region"]
        ):
            continue

        amount = t["Quantity"] * t["UnitPrice"]

        if region and t["Region"] != region:
            continue
        if min_amount and amount < min_amount:
            continue
        if max_amount and amount > max_amount:
            continue

        valid_transactions.append(t)

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary


transactions = [
  {
    'TransactionID': 'T001',
    'Date': '2024-12-01',
    'ProductID': 'P101',
    'ProductName': 'Laptop',
    'Quantity': 2,
    'UnitPrice': 45000.0,
    'CustomerID': 'C001',
    'Region': 'North'
  },
  ...
]
#calculate total revenue
def calculate_total_revenue(transactions):
    total = 0.0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total

#region wise sales 
def region_wise_sales(transactions):
    region_data = {}

    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # Calculate percentage
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions


#top selling products
def top_selling_products(transactions, n=5):
    product_data = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_data:
            product_data[name] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[name]["quantity"] += qty
        product_data[name]["revenue"] += revenue

    result = [
        (name, data["quantity"], data["revenue"])
        for name, data in product_data.items()
    ]

    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]


#customer purchase analysis
def customer_analysis(transactions):
    customers = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(t["ProductName"])

    result = {}

    for cid, data in customers.items():
        result[cid] = {
            "total_spent": data["total_spent"],
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(
                data["total_spent"] / data["purchase_count"], 2
            ),
            "products_bought": list(data["products_bought"])
        }

    return dict(
        sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True)
    )

#daily sales trend
def daily_sales_trend(transactions):
    daily = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["customers"].add(t["CustomerID"])

    result = {}

    for date in sorted(daily.keys()):
        result[date] = {
            "revenue": daily[date]["revenue"],
            "transaction_count": daily[date]["transaction_count"],
            "unique_customers": len(daily[date]["customers"])
        }

    return result

#find peak sales day
def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0
    transaction_count = 0

    for date, data in daily.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            peak_date = date
            transaction_count = data["transaction_count"]

    return peak_date, max_revenue, transaction_count
#low performing products
def low_performing_products(transactions, threshold=10):
    product_data = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_data:
            product_data[name] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[name]["quantity"] += qty
        product_data[name]["revenue"] += revenue

    result = [
        (name, data["quantity"], data["revenue"])
        for name, data in product_data.items()
        if data["quantity"] < threshold
    ]

    result.sort(key=lambda x: x[1])

    return result

