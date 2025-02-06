import pandas as pd
import argparse
import os
import sys

def read_excel_files(file_list, folder):
    """
    Reads data from multiple Excel files in a specific folder and combines them into one DataFrame.
    
    Args:
        file_list (list): List of Excel file names.
        folder (str): Folder containing the Excel files.
    
    Returns:
        pandas.DataFrame: Combined DataFrame.
    """
    combined_data = pd.DataFrame()
    for file in file_list:
        file_path = os.path.join(folder, file)
        if os.path.exists(file_path):
            print(f"Reading file: {file_path}")
            data = pd.read_excel(file_path)
            combined_data = pd.concat([combined_data, data], ignore_index=True)
        else:
            print(f"File not found: {file_path}")
    return combined_data

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Combine multiple Excel files into one.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Text file containing Excel file names.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output Excel file name.")
    args = parser.parse_args()

    # Folder where the Excel files are located
    folder = "output"
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' does not exist.")
        sys.exit(1)

    # Read the list of Excel file names from the input text file
    input_file = args.input
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    with open(input_file, 'r') as f:
        file_list = [line.strip() for line in f.readlines() if line.strip()]

    if not file_list:
        print("Error: No Excel file names found in the input file.")
        sys.exit(1)

    # Read and combine data from Excel files
    combined_data = read_excel_files(file_list, folder)

    if combined_data.empty:
        print("Error: No data found in the provided Excel files.")
        sys.exit(1)

    # Eliminate duplicate rows
    combined_data.drop_duplicates(inplace=True)

    # Sort the rows based on the 'name' column
    # if "name" in combined_data.columns:
    #     combined_data.sort_values(by="name", inplace=True)
    # else:
    #     print("Warning: 'name' column not found. Sorting skipped.")

    # Save the combined data to the output Excel file
    output_file = args.output
    combined_data.to_excel(output_file, index=False)
    print(f"Combined data saved to '{output_file}'.")

if __name__ == "__main__":
    main()
