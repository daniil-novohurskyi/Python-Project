from tkinter import Tk

from DataAnalysis import DataAnalysis
from DataAnalysisGUI import DataAnalysisGUI

if __name__ == "__main__":
    file_path = 'Dane_z_mandatów_karnych.csv'
    analysis = DataAnalysis(file_path)

    root = Tk()
    root.title("Data Analysis GUI")
    app = DataAnalysisGUI(root, analysis)
    root.mainloop()
