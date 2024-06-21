import os

import pandas as pd


def walk_dir_read(start_dir):
    # List to hold all DataFrames
    dataframes = []

    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if file_path.endswith(".csv"):
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Append the DataFrame to the list
                dataframes.append(df)

    # Concatenate all DataFrames column-wise with unique suffixes
    combined_df = pd.concat(dataframes, axis=1, ignore_index=True)

    return combined_df