import pandas as pd
from tabulate import tabulate

# Set pandas display options to show all columns, column width, and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)


def process_data(combined_df):
    """
    Processes a DataFrame by cleaning and sorting the data.

    This function performs several data cleaning tasks, including:
    - Converting the 'Data wpisu na lpt' column to datetime format.
    - Sorting the DataFrame by the 'Data wpisu na lpt' column.
    - Standardizing and trimming whitespace from string columns.
    - Removing duplicate and null rows.

    Parameters:
        combined_df (pd.DataFrame): The input DataFrame containing the data to be processed.

    Returns:
        pd.DataFrame: The cleaned and sorted DataFrame.
    """
    date_column = 'Data wpisu na lpt'  # Define the date column name
    combined_df[date_column] = combined_df[date_column].apply(convert_to_date)  # Convert date strings to datetime
    combined_df = combined_df.sort_values(by=date_column)  # Sort the DataFrame by the date column

    # Standardize and trim whitespace from string columns
    combined_df['Województwo'] = combined_df['Województwo'].str.lower().str.strip()
    combined_df['Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'] = (
        combined_df[
            'Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'].str.strip())
    combined_df['Nazwa produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'] = (
        combined_df['Nazwa produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'].str.strip())

    combined_df = combined_df.drop_duplicates()  # Remove duplicate rows
    combined_df = combined_df.dropna()  # Remove rows with null values

    return combined_df  # Return the cleaned and sorted DataFrame


def convert_to_date(date_str):
    """
    Converts a date string to the format 'YYYY-MM-DD'.

    This function attempts to convert a date string to a datetime object using
    two possible formats: '%Y-%m-%d %H:%M:%S' and '%Y-%m-%d'. If conversion
    fails, it returns None.

    Parameters:
        date_str (str): The date string to be converted.

    Returns:
        str: The formatted date string or None if conversion fails.

    Example:
        >>> convert_to_date('2023-01-01 12:34:56')
        '2023-01-01'
        >>> convert_to_date('2023-01-01')
        '2023-01-01'
        >>> convert_to_date('invalid date')
        None
    """
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):  # Loop over possible date formats
        try:
            return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')  # Try to convert and format the date
        except (ValueError, TypeError):  # Catch conversion errors and continue to the next format
            continue
    return None  # Return None if all conversions fail


def print_data_summary(df):
    """
    Prints a summary of the DataFrame.

    This function uses the tabulate library to print the DataFrame in a
    tabular format with headers and a record count.

    Parameters:
        df (pd.DataFrame): The DataFrame to be summarized.
    """
    print(tabulate(df, headers='keys', tablefmt='psql'))  # Print the DataFrame in tabular format
    print(f"The number of records: {df.shape[0]}")  # Print the number of records in the DataFrame
