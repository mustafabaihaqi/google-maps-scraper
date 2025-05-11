import pandas as pd
import argparse

def find_duplicate_addresses(input_file, output_file):
    # Load Excel file
    df = pd.read_excel(input_file)
    
    # Ensure required columns exist
    required_columns = ["name", "address"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Identify missing values
    missing = df[df['name'].isna() | df['address'].isna()]

    # Identify duplicate names
    duplicate_names = df[df.duplicated('name', keep=False)]

    # Identify duplicate addresses
    duplicate_addresses = df[df.duplicated('address', keep=False)]

    # Combine all rows and remove exact duplicates
    combined = pd.concat([missing, duplicate_names, duplicate_addresses], ignore_index=True)

    # Save to Excel
    combined.to_excel(output_file, index=False)
    
    print(f"Duplicate addresses written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find duplicate addresses in an XLSX file.")
    parser.add_argument("input_file", type=str, help="Path to the input XLSX file")
    parser.add_argument("output_file", type=str, help="Path to the output XLSX file")
    args = parser.parse_args()
    
    find_duplicate_addresses(args.input_file, args.output_file)
