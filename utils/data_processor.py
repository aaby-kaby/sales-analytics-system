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