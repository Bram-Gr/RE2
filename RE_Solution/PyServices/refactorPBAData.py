import csv
import os

# Input TXT file
input_file = r"C:\Users\b93ra\Downloads\PAS405_TRIM2025_CSV\PAS405_TRIM2025_CSV_20250825.TXT"

# Output folder for CSVs
output_folder = r"C:\Users\b93ra\Desktop\RE_REPO\RealEstate\RE_Solution\ParsedCSVs"
os.makedirs(output_folder, exist_ok=True)

# Row type headers (adjust to match your schema)
headers = {
    "OWNER": [
        "PropertyControlNumber", "RowType", "OwnerName", "MailingAddress1", "MailingAddress2",
        "MailingCityStateZip", "MailingCity", "MailingState", "MailingZip", "Extra1", "Extra2"
    ],
    "CONDO": [
        "PropertyControlNumber", "RowType", "ParcelNumber", "CondoName", "UnitNumber",
        "CondoType", "YearBuilt", "UnitDesc", "Beds", "Baths", "SquareFeet", "AssessedValue"
    ],
    "LAND": [
        "PropertyControlNumber", "RowType", "LandCode", "Acreage", "LandType", "LandValue"
    ],
    "SALE": [
        "PropertyControlNumber", "RowType", "SaleID", "SaleDate", "SaleType", "SaleAmount"
    ],
    # Add other row types if needed
}

# Prepare output CSV writers
writers = {}
files = {}

for row_type, cols in headers.items():
    out_path = os.path.join(output_folder, f"{row_type}.csv")
    f = open(out_path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(cols)
    writers[row_type] = writer
    files[row_type] = f

# Read input file
with open(input_file, newline='', encoding='latin-1') as f_in:
    reader = csv.reader(f_in)
    for row in reader:
        if len(row) < 2:
            continue
        row_type = row[1].strip().upper()
        if row_type in headers:
            # Fill missing columns with blanks if row is shorter than header
            padded_row = row[:len(headers[row_type])] + [''] * max(0, len(headers[row_type]) - len(row))
            writers[row_type].writerow(padded_row)

# Close all files
for f in files.values():
    f.close()

print(f"Parsed CSVs created in {output_folder}")
