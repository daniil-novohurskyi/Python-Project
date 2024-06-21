from tkinter import Tk

from DataAnalysis import DataAnalysis
from DataAnalysisGUI import DataAnalysisGUI
from file_handler.file_handler import walk_dir_read

if __name__ == "__main__":
    start_dir = 'data'
    combined_df = walk_dir_read(start_dir)
    analysis = DataAnalysis(combined_df)

    root = Tk()
    root.title("Data Analysis GUI")
    app = DataAnalysisGUI(root, analysis)
    root.mainloop()
