import csv

input_file = r"c:\Users\b93ra\Downloads\PAS405_TRIM2025_CSV\PAS405_TRIM2025_CSV_20250825.TXT"
output_file = r"C:\Users\b93ra\Desktop\RE_REPO\RealEstate\RE_Solution\PAS405_FLATTENED.CSV"

# Step 1: Determine max columns per row type
max_cols = {}
rows_by_type = {}

with open(input_file, newline='', encoding='latin-1') as f:
    reader = csv.reader(f)
    for row in reader:
        row_type = row[1]  # CONDO, OBY, SALE
        count = len(row)
        if row_type not in max_cols or count > max_cols[row_type]:
            max_cols[row_type] = count

# Step 2: Write flattened file
import os

CHUNK_SIZE = 100 * 1024 * 1024  # 100 MB

# List of column indexes (0-based) that are numeric and need cleaning
# Confirmed: 22 (TotalNonSchoolAssessed), 29 (TotalCommercialBldg)
NUMERIC_COLS = [22, 29]


# Enhanced cleaning and reporting
import re
def is_number(val):
    try:
        float(val)
        return True
    except:
        return False

def clean_numeric(val):
    if val.strip() == '' or is_number(val):
        return val
    return ''

non_numeric_values = {idx: set() for idx in range(50)}  # Adjust 50 if you have more columns

with open(input_file, newline='', encoding='latin-1') as f_in:
    reader = csv.reader(f_in)
    # Determine the maximum number of columns across all row types
    max_col_count = max(max_cols.values())
    header = [f'col{i+1}' for i in range(max_col_count)]

    # Print column indexes and names for user reference
    print("Column indexes and names:")
    for idx, col in enumerate(header):
        print(f"{idx}: {col}")

    chunk_idx = 1
    output_base = os.path.splitext(output_file)[0]
    output_ext = os.path.splitext(output_file)[1]
    out_path = f"{output_base}_part{chunk_idx}{output_ext}"
    f_out = open(out_path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(f_out)
    writer.writerow(header)

    for row in reader:
        row_type = row[1]
        needed_cols = max_cols[row_type]
        row += [''] * (needed_cols - len(row))
        row += [''] * (max_col_count - len(row))
        # Collect non-numeric values for reporting
        for idx in NUMERIC_COLS:
            if idx < len(row) and not (row[idx].strip() == '' or is_number(row[idx])):
                non_numeric_values[idx].add(row[idx])
            if idx < len(row):
                row[idx] = clean_numeric(row[idx])
        writer.writerow(row)
        # Check file size after writing
        if f_out.tell() >= CHUNK_SIZE:
            f_out.close()
            chunk_idx += 1
            out_path = f"{output_base}_part{chunk_idx}{output_ext}"
            f_out = open(out_path, 'w', newline='', encoding='utf-8')
            writer = csv.writer(f_out)
            writer.writerow(header)

    f_out.close()
    print(f"CSV split into {chunk_idx} file(s) of up to 100MB each, with headers. Non-numeric values in numeric columns replaced with blank.")

    # Report non-numeric values found
    print("\nNon-numeric values found in numeric columns:")
    for idx in NUMERIC_COLS:
        if non_numeric_values[idx]:
            print(f"Column {idx+1}: {non_numeric_values[idx]}")

print("Flattened CSV created:", output_file)
