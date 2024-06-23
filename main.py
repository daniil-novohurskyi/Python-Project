from tkinter import Tk

from DataAnalysis import DataAnalysis
from DataAnalysisGUI import DataAnalysisGUI
from handler.data_handler import process_data, print_data_summary
from handler.file_handler import walk_dir_read

if __name__ == "__main__":
    start_dir = 'data'
    combined_df = walk_dir_read(start_dir)
    processed_df = process_data(combined_df)
    # print_data_summary(combined_df)
    print_data_summary(processed_df)

    analysis = DataAnalysis(processed_df)

    root = Tk()
    root.title("RegionalProductAnalyzer")
    root.attributes('-fullscreen', True)
    app = DataAnalysisGUI(root, analysis)
    root.mainloop()
