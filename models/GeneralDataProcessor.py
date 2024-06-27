import pandas as pd


class GeneralDataProcessor:
    """
    A class to process and analyze general data statistics based on grouped data.

    Attributes:
        raw_data (DataFrame): The raw data to be processed.
        statistic_title (str): Title for the statistics being analyzed.
        type_for_analyse (str): Type of data being analyzed.
        stat_data (dict): Dictionary to store statistical data by group.
        stat_summary (dict): Dictionary to store summary statistics for all data.

    Methods:
        __process_data(column_group):
            Processes the raw data by grouping and computing statistics for each group.
    """

    def __init__(self, raw_data, column_group, statistic_title, type_for_analyse):
        """
        Initializes the GeneralDataProcessor instance.

        Args:
            raw_data (DataFrame): The raw data to be processed.
            column_group (str): The column name to group the data by.
            statistic_title (str): Title for the statistics being analyzed.
            type_for_analyse (str): Type of data being analyzed.
        """
        self.raw_data = raw_data
        self.statistic_title = statistic_title
        self.type_for_analyse = type_for_analyse
        self.stat_data = {}  # Initialize an empty dictionary for storing grouped data statistics
        self.stat_summary = {}  # Initialize an empty dictionary for storing summary statistics
        self.__process_data(column_group)  # Process the raw data to populate stat_data and stat_summary

    def __process_data(self, column_group):
        """
        Processes the raw data by grouping and computing statistics for each group.

        Args:
            column_group (str): The column name to group the data by.
        """
        # Group the raw data by the specified column
        grouped = self.raw_data.groupby(column_group)

        # List to store counts for computing overall statistics
        all_counts = []

        # Iterate over each group and calculate statistics
        for product, group_data in grouped:
            count_records = len(group_data)  # Count records in each group
            self.stat_data[product] = count_records  # Store count in stat_data dictionary
            all_counts.append(count_records)  # Append count to all_counts list

        # Create a DataFrame from all_counts data
        all_data_df = pd.DataFrame(all_counts, columns=['counts'])

        # Compute statistical measures
        mean_val = all_data_df['counts'].mean()
        median_val = all_data_df['counts'].median()
        mode_val = all_data_df['counts'].mode().iloc[0] if not all_data_df['counts'].mode().empty else None
        variance_val = all_data_df['counts'].var(ddof=1)

        # Round the computed values
        mean_val = round(mean_val, 2)
        median_val = round(median_val, 2)
        mode_val = round(mode_val, 2) if mode_val is not None else None
        variance_val = round(variance_val, 2)

        # Store summary statistics in stat_summary dictionary
        self.stat_summary = {
            'mean': mean_val,
            'median': median_val,
            'mode': mode_val,
            'variance': variance_val
        }
