import pandas as pd


class PlotProcessor:
    """
    Prepares and filters data for plotting and analysis.

    Attributes:
        data (pd.DataFrame): The input data containing records.

    Methods:
        prepare_data():
            Adjusts column names and converts date columns for further analysis.
        get_data_by_date(start_date, end_date):
            Retrieves filtered data between specified dates.

    Example usage:
        processor = PlotProcessor(dataframe)
        processor.prepare_data()
        filtered_data = processor.get_data_by_date('2023-01-01', '2023-12-31')
    """

    def __init__(self, dataframe):
        """
        Initializes the PlotProcessor instance.

        Args:
            dataframe (pd.DataFrame): The input data containing records.
        """
        self.data = dataframe  # Initialize the data attribute with the input dataframe
        self.prepare_data()  # Call prepare_data method upon initialization

    def prepare_data(self):
        """
        Prepares the data by adjusting column names and converting date columns.
        """
        # Adjust column names to remove newline characters and strip whitespace
        self.data.columns = self.data.columns.str.replace('\n', '').str.strip()

        # Convert 'Data wpisu na lpt' column to datetime format
        self.data['Data wpisu na lpt'] = pd.to_datetime(self.data['Data wpisu na lpt'], errors='coerce')

        # Extract year from 'Data wpisu na lpt' column and create a new 'Year' column
        self.data['Year'] = self.data['Data wpisu na lpt'].dt.year

    def get_data_by_date(self, start_date, end_date):
        """
        Retrieves filtered data between specified dates.

        Args:
            start_date (str): Start date in 'YYYY-MM-DD' format.
            end_date (str): End date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: Filtered DataFrame containing records between start_date and end_date.
        """
        # Filter data based on 'Data wpisu na lpt' column within the specified date range
        filtered_data = self.data[
            (self.data['Data wpisu na lpt'] >= start_date) & (self.data['Data wpisu na lpt'] <= end_date)
            ]
        return filtered_data
