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
from utils.data_processor import parse_transactions, validate_and_filter

raw_lines = read_sales_data("data/sales_data.txt")
transactions = parse_transactions(raw_lines)

valid_txns, invalid_count, summary = validate_and_filter(
    transactions,
    region="North",
    min_amount=20000
)

print("Valid transactions:", len(valid_txns))
print("Invalid transactions:", invalid_count)
print("Summary:", summary)
