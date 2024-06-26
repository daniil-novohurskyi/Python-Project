from tkinter import Tk

from apps.DataAnalysisApp import DataAnalysisApp
from apps.StatisticsMapApp import StatisticsMapApp
from handler.data_handler import process_data, print_data_summary
from handler.file_handler import walk_dir_read

if __name__ == "__main__":
    start_dir = 'data'
    combined_df = walk_dir_read(start_dir)
    processed_df = process_data(combined_df)
    # print_data_summary(combined_df)
    print_data_summary(processed_df)

    # root = Tk()
    # root.title("RegionalProductAnalyzer")
    # root.attributes('-fullscreen', True)
    # app = StatisticsMapApp(root, processed_df)
    # app.run()

    root = Tk()
    root.title("RegionalProductAnalyzer")
    root.attributes('-fullscreen', True)
    app = DataAnalysisApp(root, processed_df)
    app.run()
