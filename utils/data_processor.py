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
