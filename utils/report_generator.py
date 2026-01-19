from datetime import datetime
from collections import defaultdict
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted(t["Date"] for t in transactions)
    start_date = dates[0] if dates else "N/A"
    end_date = dates[-1] if dates else "N/A"

    region_data = region_wise_sales(transactions)
    top_products = top_selling_products(transactions)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
    enrichment_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0
    failed_products = [t["ProductName"] for t in enriched_transactions if not t.get("API_Match")]

    with open(output_file, "w", encoding="utf-8") as f:

        # 1. HEADER
        f.write("=" * 50 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_transactions}\n")
        f.write("=" * 50 + "\n\n")

        # 2. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {start_date} to {end_date}\n\n")

        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<15}{'Transactions'}\n")

        for region, data in region_data.items():
            f.write(
                f"{region:<10}₹{data['total_sales']:,.0f}<15"
                f"{data['percentage']:.2f}%<15"
                f"{data['transaction_count']}\n"
            )
        f.write("\n")

        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<5}{'Product':<25}{'Qty':<10}{'Revenue'}\n")

        for i, (name, qty, revenue) in enumerate(top_products, 1):
            f.write(f"{i:<5}{name:<25}{qty:<10}₹{revenue:,.2f}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<5}{'Customer':<15}{'Spent':<15}{'Orders'}\n")

        for i, (cid, data) in enumerate(list(customers.items())[:5], 1):
            f.write(
                f"{i:<5}{cid:<15}₹{data['total_spent']:,.2f}<15"
                f"{data['purchase_count']}\n"
            )
        f.write("\n")

        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Date':<12}{'Revenue':<15}{'Txns':<10}{'Customers'}\n")

        for date, data in daily_trend.items():
            f.write(
                f"{date:<12}₹{data['revenue']:,.2f}<15"
                f"{data['transaction_count']:<10}"
                f"{data['unique_customers']}\n"
            )
        f.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 50 + "\n")
        f.write(f"Best Selling Day: {peak_day[0]} | Revenue: ₹{peak_day[1]:,.2f}\n\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for p in low_products:
                f.write(f"- {p[0]} (Qty: {p[1]}, Revenue: ₹{p[2]:,.2f})\n")
        else:
            f.write("No low performing products.\n")
        f.write("\n")

        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {enrichment_rate:.2f}%\n")

        if failed_products:
            f.write("Products Not Enriched:\n")
            for p in set(failed_products):
                f.write(f"- {p}\n")

    print(f"Report generated successfully: {output_file}")
