import csv
import os

# Input TXT file - using the local copy
input_file = r"C:\Users\b93ra\Desktop\RE_REPO\RealEstate\RE_Solution\PyServices\PAS405_TRIM2025_CSV_20250825.TXT"

# Output folder for CSVs
output_folder = r"C:\Users\b93ra\Desktop\RE_REPO\RealEstate\RE_Solution\ParsedCSVs"
os.makedirs(output_folder, exist_ok=True)

# Read the actual header from the file to get correct field names
with open(input_file, 'r', encoding='latin-1') as f:
    header_line = f.readline().strip()
    all_fields = header_line.split(',')

print(f"Found {len(all_fields)} fields in header:")
for i, field in enumerate(all_fields):
    print(f"  {i:2d}: {field}")

# Define field mappings based on actual data structure analysis and CAMA documentation
# Each record type gets relevant fields mapped to their correct positions
row_type_mappings = {
    "PARCEL": [
        "PropertyControlNumber", "RecordType", "Field2", "SitusAddressNumber", "Field4", "Field5", 
        "SitusStreetName", "SitusStreetSuffix", "Field8", "SitusCity", "Field10", 
        "Field11", "SitusZip", "LandUseCode", "LandUseDescription", "TotalMarketValue",
        "TotalAssessedValue", "Field17", "TotalImprovementValue", "TotalLandValue",
        "Field20", "Field21", "Field22", "Field23", "Field24", "Field25"
    ],
    "OWNER": [
        "PropertyControlNumber", "RecordType", "OwnerName", "MailingAddress1", 
        "MailingAddress2", "MailingCityStateZip", "LegalDescription", "LegalDescription2", "LegalDescription3"
    ],
    "LAND": [
        "PropertyControlNumber", "RecordType", "LandSequence", "LandTypeCode", "LandTypeDescription",
        "LandUseCode", "LandUseDescription", "LandClassificationCode", "LandClassificationDescription", "LandAGFlag", 
        "Field10", "Field11", "Field12", "LandLocation", "LandID",
        "Acreage", "Field16", "Field17", "Field18", "LandValue", "Field20"
    ],
    "OBY": [
        "PropertyControlNumber", "RecordType", "OBYSequence1", "OBYSequence2", 
        "OBYTypeCode", "OBYDescription", "Field6", "Field7", "OBYCategory",
        "OBYSize", "OBYUnitValue", "OBYYear", "Field12", "OBYTotalValue"
    ],
    "SALE": [
        "PropertyControlNumber", "RecordType", "SaleInstrument1", "SaleBook1", 
        "SaleDate1", "SaleInstrumentType1", "SaleValidityCode1", "SaleValidationCode1", "SaleAmount1", 
        "SaleInstrument2", "SaleBook2", "SaleDate2", "SaleInstrumentType2", "SaleValidityCode2", 
        "SaleValidationCode2", "SaleAmount2", "SaleInstrument3", "SaleBook3", "SaleDate3",
        "SaleInstrumentType3", "SaleValidityCode3", "SaleValidationCode3", "SaleAmount3", "Field23",
        "Field24", "Field25", "Field26", "Field27", "Field28", "Field29", "Field30",
        "Field31", "Field32", "Field33", "Field34", "Field35", "Field36"
    ],
    "RESBLD": [
        "PropertyControlNumber", "RecordType", "BuildingSequence", "BuildingClassificationCode", 
        "BuildingType", "YearBuilt", "YearEffective", "Field7", 
        "Bedrooms", "HalfBaths", "Bathrooms", "Field11", "ExteriorWall", 
        "Field13", "Field14", "Field15", "RoofStructure", "Field17", "RoofCover", "Field19",
        "InteriorWall", "Field21", "Field22", "FloorType", "Field24", "Field25", "Field26",
        "HeatCode", "HeatDescription", "HeatSystemType", "HeatSystemDescription", "HeatFuelType", "HeatFuelDescription", "GradeCode",
        "GradeDescription", "ConditionCode", "ConditionDescription", "Field37", "Field38", "SquareFeet", "Field40", "BuildingValue"
    ],
    "COMBLD": [
        "PropertyControlNumber", "RecordType", "BuildingSequence", "StructureCode", 
        "StructureDescription", "YearBuilt", "YearEffective", "Field7", 
        "Stories", "ExtWallCode", "ExtWallDescription", "InteriorFinish", "InteriorFinishDescription", "ConstructionType",
        "ConstructionTypeDescription", "AirConditioningCode", "AirConditioningDescription", "GradeCode", "GradeDescription", "Field19",
        "Field20", "Field21", "BuildingValue"
    ],
    "CONDO": [
        "PropertyControlNumber", "RecordType", "CondoParcelNumber", "CondoProjectName",
        "Field4", "UnitSequence", "UnitClassificationCode", "UnitClassificationDescription", "YearBuilt", 
        "UnitDesignation", "UnitDescription", "Bedrooms", "Bathrooms", 
        "HalfBaths", "SquareFeet", "UnitValue", "Field16"
    ]
}

# Open output CSVs
writers = {}
files = {}
for rtype, headers in row_type_mappings.items():
    out_path = os.path.join(output_folder, f"{rtype}.csv")
    f = open(out_path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(headers)
    writers[rtype] = writer
    files[rtype] = f

# Process input file
with open(input_file, newline='', encoding='latin-1') as f_in:
    # Skip the header line
    header = f_in.readline()
    
    reader = csv.reader(f_in)
    record_counts = {}
    
    for row in reader:
        if len(row) < 2:
            continue
            
        property_control_number = row[0].strip()
        record_type = row[1].strip().upper()
        
        # Count records by type
        if record_type not in record_counts:
            record_counts[record_type] = 0
        record_counts[record_type] += 1
        
        # Only process known record types
        if record_type not in row_type_mappings:
            print(f"Unknown record type: {record_type}")
            continue

        # Create output row based on record type
        headers = row_type_mappings[record_type]
        csv_row = [''] * len(headers)
        
        # Map the data based on record type
        if record_type == "PARCEL":
            # For PARCEL records, map all 33 fields directly
            for i in range(min(len(row), len(csv_row))):
                csv_row[i] = row[i].strip() if i < len(row) else ''
                
        elif record_type == "OWNER":
            # Map OWNER specific fields
            csv_row[0] = property_control_number  # PropertyControlNumber
            csv_row[1] = record_type              # RecordType
            if len(row) > 2: csv_row[2] = row[2].strip()  # OwnerName
            if len(row) > 3: csv_row[3] = row[3].strip()  # MailingAddress1
            if len(row) > 4: csv_row[4] = row[4].strip()  # MailingAddress2
            if len(row) > 5: csv_row[5] = row[5].strip()  # MailingCityStateZip
            if len(row) > 6: csv_row[6] = row[6].strip()  # OwnerInfo
            if len(row) > 7: csv_row[7] = row[7].strip()  # Extra1
            if len(row) > 8: csv_row[8] = row[8].strip()  # Extra2
            
        elif record_type == "LAND":
            # Map LAND specific fields
            csv_row[0] = property_control_number  # PropertyControlNumber
            csv_row[1] = record_type              # RecordType
            for i in range(2, min(len(row), len(csv_row))):
                csv_row[i] = row[i].strip() if i < len(row) else ''
                
        elif record_type == "OBY":
            # Map OBY specific fields
            csv_row[0] = property_control_number  # PropertyControlNumber
            csv_row[1] = record_type              # RecordType
            for i in range(2, min(len(row), len(csv_row))):
                csv_row[i] = row[i].strip() if i < len(row) else ''
                
        elif record_type == "SALE":
            # Map SALE specific fields
            csv_row[0] = property_control_number  # PropertyControlNumber
            csv_row[1] = record_type              # RecordType
            for i in range(2, min(len(row), len(csv_row))):
                csv_row[i] = row[i].strip() if i < len(row) else ''
                
        elif record_type == "RESBLD":
            # Map RESBLD specific fields
            csv_row[0] = property_control_number  # PropertyControlNumber
            csv_row[1] = record_type              # RecordType
            for i in range(2, min(len(row), len(csv_row))):
                csv_row[i] = row[i].strip() if i < len(row) else ''
                
        elif record_type == "COMBLD":
            # Map COMBLD specific fields
            csv_row[0] = property_control_number  # PropertyControlNumber
            csv_row[1] = record_type              # RecordType
            for i in range(2, min(len(row), len(csv_row))):
                csv_row[i] = row[i].strip() if i < len(row) else ''
                
        elif record_type == "CONDO":
            # Map CONDO specific fields
            csv_row[0] = property_control_number  # PropertyControlNumber
            csv_row[1] = record_type              # RecordType
            for i in range(2, min(len(row), len(csv_row))):
                csv_row[i] = row[i].strip() if i < len(row) else ''
                
        writers[record_type].writerow(csv_row)

# Close all files
for f in files.values():
    f.close()

print(f"Parsed CSVs created in {output_folder}")
print("Record counts by type:")
for rtype, count in record_counts.items():
    print(f"  {rtype}: {count}")
