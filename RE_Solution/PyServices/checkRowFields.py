import csv

# Path to your raw TXT
input_file = r"C:\Users\b93ra\Downloads\PAS405_TRIM2025_CSV\PAS405_TRIM2025_CSV_20250825.TXT"

row_types = set()

with open(input_file, newline='', encoding='latin-1') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 1:
            row_types.add(row[1].strip().upper())

print("Unique RowTypes found in file:")
for rt in sorted(row_types):
    print(rt)
