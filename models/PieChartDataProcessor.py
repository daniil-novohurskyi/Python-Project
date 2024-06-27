import pandas as pd


class PieChartDataProcessor:
    """
    Processes raw data to generate statistics by region across product types.

    Attributes:
        raw_data (pd.DataFrame): The raw input data.
        stat_data (dict): Dictionary storing region-wise product counts.
        stat_summary (dict): Dictionary storing summary statistics for each region.

    Methods:
        __process_data():
            Private method to calculate product counts and summary statistics for each region.
    """

    def __init__(self, raw_data):
        """
        Initializes the PieChartDataProcessor instance.

        Args:
            raw_data (pd.DataFrame): The raw input data.
        """
        self.raw_data = raw_data
        self.stat_data = {}  # Initialize an empty dictionary to store region-wise product counts
        self.stat_summary = {}  # Initialize an empty dictionary to store summary statistics
        self.__process_data()  # Call the private method to process the data upon initialization

    def __process_data(self):
        """
        Processes the raw data to calculate product counts and summary statistics for each region.
        """
        # Group the raw data by region ('Województwo')
        grouped = self.raw_data.groupby('Województwo')

        # Iterate through each region and its corresponding group data
        for region, group_data in grouped:
            # Calculate product counts for the current region
            product_counts = group_data[
                'Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'].value_counts().to_dict()

            # Store the product counts in the stat_data dictionary under the region key
            self.stat_data[region] = product_counts

            # Convert product counts dictionary to a DataFrame for summary statistics calculation
            product_counts_df = pd.DataFrame.from_dict(product_counts, orient='index', columns=['counts'])

            # Calculate mean, median, mode, and variance of product counts
            mean_val = product_counts_df['counts'].mean()
            median_val = product_counts_df['counts'].median()
            mode_val = product_counts_df['counts'].mode()[0] if not product_counts_df['counts'].mode().empty else None
            variance_val = product_counts_df['counts'].var(ddof=1)

            # Store the summary statistics in the stat_summary dictionary under the region key
            self.stat_summary[region] = {
                'mean': mean_val,
                'median': median_val,
                'mode': mode_val,
                'variance': variance_val
            }
