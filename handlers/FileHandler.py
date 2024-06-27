import csv
import os
import pandas as pd


def walk_dir_read(start_dir):
    """
    Reads all CSV files from the given directory and its subdirectories,
    combines them into a single DataFrame.

    This function walks through the directory tree, reads all CSV files,
    and combines their data into one DataFrame. It ensures that the column
    names are consistent across all files.

    Parameters:
        start_dir (str): The starting directory to walk through and read CSV files.

    Returns:
        pd.DataFrame: A combined DataFrame containing data from all CSV files.
    """
    dataframes = []  # List to hold individual DataFrames
    first_frame = True  # Flag to check if the first CSV file is being processed
    column_names = None  # Variable to store column names

    # Walk through the directory tree starting from 'start_dir'
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)  # Get the full file path
            if file_path.endswith(".csv"):  # Check if the file is a CSV file
                if first_frame:
                    # If processing the first CSV file, read and store column names
                    with open(file_path, 'r', newline='', encoding='utf-8') as file:
                        reader = csv.reader(file)
                        first_row = next(reader)  # Read the first row (column names)
                        column_names = first_row  # Store column names
                        first_frame = False  # Set flag to False after processing the first file
                # Open the CSV file and check if the column names match
                with open(file_path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    first_row = next(reader)  # Read the first row
                    skip_line = 1 if first_row == column_names else 0  # Determine if the first row should be skipped
                df = pd.read_csv(file_path, skiprows=skip_line)  # Read the CSV file into a DataFrame
                df.columns = column_names  # Set the DataFrame columns to the stored column names
                dataframes.append(df)  # Append the DataFrame to the list

    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df  # Return the combined DataFrame
