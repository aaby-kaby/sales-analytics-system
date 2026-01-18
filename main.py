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