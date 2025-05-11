import pandas as pd
import argparse
import os

def remove_duplicates(input_file, output_file):
    # Load the Excel file
    df = pd.read_excel(input_file)
    
    # Check if 'name' column exists
    if 'name' not in df.columns:
        print("Error: The 'name' column is missing from the file.")
        return
    
    # Remove rows based on the absence duplication and of 'name' and 'address' column's value from an Excel file, keeping the first occurrence
    df_cleaned = (
        df.dropna(subset=['name', 'address'])
        .drop_duplicates(subset='name', keep='first')
        .drop_duplicates(subset='address', keep='first')
    )

    # Save the cleaned data to a new Excel file
    df_cleaned.to_excel(output_file, index=False)
    print(f"Absences and duplicates removed. Cleaned file saved as: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove rows based on the absence duplication and of 'name' and 'address' column's value from an Excel file.")
    parser.add_argument("input_file", help="Path to the input Excel file")
    parser.add_argument("output_file", help="Path to save the cleaned Excel file")
    args = parser.parse_args()
    
    # Check if the input file exists
    if not os.path.exists(args.input_file):
        print("Error: Input file does not exist.")
    else:
        remove_duplicates(args.input_file, args.output_file)
