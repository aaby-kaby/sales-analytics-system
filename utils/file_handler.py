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


def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw transaction lines
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()

                raw_lines = []
                for line in lines[1:]:  # skip header
                    line = line.strip()
                    if line:
                        raw_lines.append(line)

                return raw_lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print("Error: File not found")
            return []

    print("Error: Unable to read file with supported encodings")
    return []
