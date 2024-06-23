import pandas as pd
from tabulate import tabulate

# maximum console output sizes settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)


def process_data(combined_df):
    # 1. sorting by time
    date_column = 'Data wpisu na lpt'
    combined_df[date_column] = combined_df[date_column].apply(convert_to_date)
    combined_df = combined_df.sort_values(by=date_column)
    combined_df[date_column] = pd.to_datetime(combined_df[date_column])

    # 2. bringing to a single appearance
    combined_df['Województwo'] = combined_df['Województwo'].str.lower().str.strip()
    combined_df['Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'] = (
        combined_df['Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'].str.strip())
    combined_df['Nazwa produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'] = (
        combined_df['Nazwa produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'].str.strip())

    # 3. drop duplicates and NaN's
    combined_df = combined_df.drop_duplicates()
    combined_df = combined_df.dropna()

    return combined_df


def convert_to_date(date_str):
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            continue
    return None


def print_data_summary(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))
    print(f"The number of records: {df.shape[0]}")
