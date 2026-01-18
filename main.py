from utils.file_handler import read_sales_file
from utils.data_processor import clean_sales_data
from utils.api_handler import fetch_product_category

raw_data, total = read_sales_file("data/sales_data.txt")
clean_data = clean_sales_data(raw_data)

total_revenue = 0
region_sales = {}

for record in clean_data:
    revenue = record["Quantity"] * record["UnitPrice"]
    total_revenue += revenue
    region = record["Region"]
    region_sales[region] = region_sales.get(region, 0) + revenue

print("\nTotal Revenue:", total_revenue)
print("Sales by Region:", region_sales)

# Generate Output Report
with open("output/sales_report.txt", "w") as file:
    file.write(f"Total Revenue: {total_revenue}\n")
    file.write("Sales by Region:\n")
    for r, v in region_sales.items():
        file.write(f"{r}: {v}\n")



from utils.file_handler import read_sales_data

raw_lines = read_sales_data("data/sales_data.txt")
print(len(raw_lines))
print(raw_lines[:2])


from utils.data_processor import parse_transactions

transactions = parse_transactions(raw_lines)
print(len(transactions))
print(transactions[0])






from utils.file_handler import read_sales_data
from utils.data_processor import *

raw_lines = read_sales_data("data/sales_data.txt")
transactions = parse_transactions(raw_lines)

valid_transactions, invalid_count, summary = validate_and_filter(
    transactions,
    region=None,
    min_amount=None,
    max_amount=None
)
print("Valid transactions:", len(valid_transactions))
print("Invalid transactions:", invalid_count)
print("Summary:", summary)


print("\nTotal Revenue:")
print(calculate_total_revenue(valid_transactions))

print("\nRegion Wise Sales:")
print(region_wise_sales(valid_transactions))

print("\nTop Selling Products:")
print(top_selling_products(valid_transactions))

print("\nCustomer Analysis:")
print(customer_analysis(valid_transactions))

print("\nDaily Sales Trend:")
print(daily_sales_trend(valid_transactions))

print("\nPeak Sales Day:")
print(find_peak_sales_day(valid_transactions))

print("\nLow Performing Products:")
print(low_performing_products(valid_transactions))