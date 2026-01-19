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

    with open(output_file, "w", encoding="utf-8") as f:

        # ================= HEADER =================
        f.write("=" * 50 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {len(transactions)}\n")
        f.write("=" * 50 + "\n\n")

        # ================= OVERALL SUMMARY =================
        total_revenue = calculate_total_revenue(transactions)
        avg_order_value = total_revenue / len(transactions) if transactions else 0

        dates = sorted(t["Date"] for t in transactions)
        date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {len(transactions)}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        # ================= REGION-WISE PERFORMANCE =================
        region_stats = region_wise_sales(transactions)

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Region':<10}{'Sales':>15}{'% of Total':>15}{'Transactions':>15}\n")

        for region, data in region_stats.items():
            f.write(
                f"{region:<10}"
                f"₹{data['total_sales']:>14,.2f}"
                f"{data['percentage']:>14.2f}%"
                f"{data['transaction_count']:>15}\n"
            )
        f.write("\n")

        # ================= TOP 5 PRODUCTS =================
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<5}{'Product':<25}{'Qty Sold':>10}{'Revenue':>15}\n")

        top_products = top_selling_products(transactions, n=5)
        for i, (name, qty, revenue) in enumerate(top_products, start=1):
            f.write(f"{i:<5}{name:<25}{qty:>10}{revenue:>15,.2f}\n")
        f.write("\n")

        # ================= TOP 5 CUSTOMERS =================
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<5}{'Customer ID':<15}{'Total Spent':>15}{'Orders':>10}\n")

        customers = customer_analysis(transactions)
        top_customers = list(customers.items())[:5]

        for i, (cid, data) in enumerate(top_customers, start=1):
            f.write(
                f"{i:<5}{cid:<15}"
                f"{data['total_spent']:>15,.2f}"
                f"{data['purchase_count']:>10}\n"
            )
        f.write("\n")

        # ================= DAILY SALES TREND =================
        f.write("DAILY SALES TREND\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>15}{'Txns':>10}{'Customers':>12}\n")

        daily_trend = daily_sales_trend(transactions)
        for date, data in daily_trend.items():
            f.write(
                f"{date:<12}"
                f"{data['revenue']:>15,.2f}"
                f"{data['transaction_count']:>10}"
                f"{data['unique_customers']:>12}\n"
            )
        f.write("\n")

        # ================= PRODUCT PERFORMANCE =================
        best_day = find_peak_sales_day(transactions)
        low_products = low_performing_products(transactions)

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 50 + "\n")
        f.write(f"Best Selling Day: {best_day[0]} | Revenue: ₹{best_day[1]:,.2f} | Transactions: {best_day[2]}\n\n")

        f.write("Low Performing Products:\n")
        if low_products:
            for name, qty, rev in low_products:
                f.write(f"- {name}: Qty {qty}, Revenue ₹{rev:,.2f}\n")
        else:
            f.write("None\n")
        f.write("\n")

        # ================= API ENRICHMENT SUMMARY =================
        total_enriched = sum(1 for t in enriched_transactions if t.get("API_Match"))
        success_rate = (total_enriched / len(enriched_transactions)) * 100 if enriched_transactions else 0

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Products Enriched: {total_enriched}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")

        failed_products = {
            t["ProductName"] for t in enriched_transactions if not t.get("API_Match")
        }

        if failed_products:
            f.write("Products Not Enriched:\n")
            for p in failed_products:
                f.write(f"- {p}\n")
        else:
            f.write("All products enriched successfully\n")

    print(f"Sales report generated at {output_file}")
