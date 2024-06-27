import pandas as pd


class MapDataProcessor:
    """
    Processes raw data to generate statistics by product type across regions.

    Attributes:
        raw_data (pd.DataFrame): The raw input data.
        stat_data (dict): Dictionary storing product-wise region counts.
        stat_summary (dict): Dictionary storing summary statistics for each product.

    Methods:
        __process_data():
            Private method to calculate region counts and summary statistics for each product type.
    """

    def __init__(self, raw_data):
        """
        Initializes the MapDataProcessor instance.

        Args:
            raw_data (pd.DataFrame): The raw input data.
        """
        self.raw_data = raw_data
        self.stat_data = {}  # Initialize an empty dictionary to store product-wise region counts
        self.stat_summary = {}  # Initialize an empty dictionary to store summary statistics
        self.__process_data()  # Call the private method to process the data upon initialization

    def __process_data(self):
        """
        Processes the raw data to calculate region counts and summary statistics for each product type.
        """
        # Group the raw data by product type
        grouped = self.raw_data.groupby(
            'Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt')

        # Iterate through each product type and its corresponding group data
        for product, group_data in grouped:
            # Calculate region counts for the current product type
            region_counts = group_data['Województwo'].value_counts().to_dict()

            # Store the region counts in the stat_data dictionary under the product type key
            self.stat_data[product] = region_counts

            # Convert region counts dictionary to a DataFrame for summary statistics calculation
            region_counts_df = pd.DataFrame.from_dict(region_counts, orient='index', columns=['counts'])

            # Calculate mean, median, mode, and variance of region counts
            mean_val = region_counts_df['counts'].mean()
            mean_val = round(mean_val, 2)
            median_val = region_counts_df['counts'].median()
            median_val = round(median_val, 2)
            mode_val = region_counts_df['counts'].mode()[0] if not region_counts_df['counts'].mode().empty else None
            mode_val = round(mode_val, 2) if mode_val is not None else None
            variance_val = region_counts_df['counts'].var(ddof=1)
            variance_val = round(variance_val, 2)

            # Store the summary statistics in the stat_summary dictionary under the product type key
            self.stat_summary[product] = {
                'średnia': mean_val,
                'mediana': median_val,
                'moda': mode_val,
                'wariancja': variance_val
            }
