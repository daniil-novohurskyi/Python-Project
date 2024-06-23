import os
import csv
import pandas as pd
from tabulate import tabulate


def walk_dir_read(start_dir):
    # maximum console output sizes settings
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

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

    # manipulations with data
    # 1. sorting by time
    date_column = 'Data wpisu na lpt'

    def convert_to_date(date_str):
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
            try:
                return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                continue
        return None

    combined_df[date_column] = combined_df[date_column].apply(convert_to_date)
    combined_df = combined_df.sort_values(by=date_column)
    combined_df[date_column] = pd.to_datetime(combined_df[date_column])

    # 2. bringing provinces to a single appearance
    combined_df['Województwo'] = combined_df['Województwo'].str.lower().str.strip()

    # 3. drop duplicates and NaN's
    combined_df = combined_df.drop_duplicates()
    combined_df = combined_df.dropna()

    # if you need to check for a specific province
    # provinces = [
    #     'dolnośląskie', 'kujawsko-pomorskie', 'lubelskie', 'lubuskie', 'łódzkie',
    #     'małopolskie', 'mazowieckie', 'opolskie', 'podkarpackie', 'podlaskie',
    #     'pomorskie', 'śląskie', 'świętokrzyskie', 'warmińsko-mazurskie',
    #     'wielkopolskie', 'zachodniopomorskie'
    # ]
    # combined_df = combined_df[~combined_df['Województwo'].isin(provinces)]

    # output of the received data collection
    print(tabulate(combined_df, headers='keys', tablefmt='psql'))
    print(f"The number of records: {combined_df.shape[0]}")

    return combined_df
