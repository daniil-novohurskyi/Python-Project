import os
import csv
import pandas as pd


def walk_dir_read(start_dir):
    # List to hold all DataFrames
    dataframes = []
    first_frame = True
    column_names = None
    skip_line = None
    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if file_path.endswith(".csv"):
                # Read the CSV file
                if first_frame:
                    with open(file_path, 'r', newline='', encoding='utf-8') as file:
                        # Create a CSV reader object
                        reader = csv.reader(file)
                        # Read the first row (header)
                        first_row = next(reader)
                    # Extract column names from the first row
                        column_names = first_row
                        first_frame = False
                with open(file_path, 'r', newline='', encoding='utf-8') as file:
                    # Create a CSV reader object
                    reader = csv.reader(file)
                    # Read the first row (header)
                    first_row = next(reader)
                    skip_line = 1 if first_row == column_names else 0
                df = pd.read_csv(file_path, skiprows=skip_line)
                df.columns = column_names
                # Append the DataFrame to the list
                dataframes.append(df)

    # Concatenate all DataFrames column-wise with unique suffixes
    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df