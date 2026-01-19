# main.py

from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
from utils.report_generator import generate_sales_report


def main():
    print("=" * 50)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 50)

    try:
        # [1/10] Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # [2/10] Parse & clean
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # [3/10] Show filter options
        print("\n[3/10] Filter Options Available:")
        valid_txns_preview, _, _ = validate_and_filter(transactions)
        regions = {t["Region"] for t in valid_txns_preview}
        amounts = [t["Quantity"] * t["UnitPrice"] for t in valid_txns_preview]

        print("Regions:", ", ".join(sorted(regions)))
        print(f"Amount Range: ₹{int(min(amounts))} - ₹{int(max(amounts))}")

        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amount = None
        max_amount = None

        if choice == "y":
            region = input("Enter region (or press Enter to skip): ").strip() or None
            min_amount = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amount = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amount = float(min_amount) if min_amount else None
            max_amount = float(max_amount) if max_amount else None

        # [4/10] Validate & filter
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amount,
            max_amount=max_amount
        )
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # [5/10] Analytics
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # [6/10] Fetch API data
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enrich sales data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
        success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({success_rate:.1f}%)")

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9/10] Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # [10/10] Done
        print("\n[10/10] Process Complete!")
        print("=" * 50)

    except Exception as e:
        print("\n❌ An error occurred:")
        print(str(e))


if __name__ == "__main__":
    main()
