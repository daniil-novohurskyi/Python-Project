from tkinter import Tk

from DataAnalysis import DataAnalysis
from DataAnalysisGUI import DataAnalysisGUI

if __name__ == "__main__":
    file_path = 'Produkty_regionalne_stan_na_05_01_22_r.csv'
    analysis = DataAnalysis(file_path)

    root = Tk()
    root.title("Data Analysis GUI")
    app = DataAnalysisGUI(root, analysis)
    root.mainloop()