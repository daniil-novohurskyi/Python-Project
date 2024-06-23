import csv
import os
import pandas as pd


def walk_dir_read(start_dir):

    dataframes = []
    first_frame = True
    column_names = None

    # passing through the directory
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if file_path.endswith(".csv"):
                if first_frame:
                    with open(file_path, 'r', newline='', encoding='utf-8') as file:
                        reader = csv.reader(file)
                        first_row = next(reader)
                        column_names = first_row
                        first_frame = False
                with open(file_path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    first_row = next(reader)
                    skip_line = 1 if first_row == column_names else 0
                df = pd.read_csv(file_path, skiprows=skip_line)
                df.columns = column_names
                dataframes.append(df)
                # output of the received data from the file
                # print(f"Data from file {filename}:")
                # print(tabulate(df, headers='keys', tablefmt='psql'))

    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df
