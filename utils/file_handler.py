def read_sales_file(file_path):
    records = []
    total_lines = 0

    try:
        with open(file_path, "r", encoding="latin-1") as file:
            for line in file:
                total_lines += 1
                line = line.strip()
                if line:
                    records.append(line)
    except FileNotFoundError:
        print("Sales file not found")

    return records, total_lines