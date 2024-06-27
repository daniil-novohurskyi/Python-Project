import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class GeneralDataProcessor:
    def __init__(self, raw_data, column_group):
        self.raw_data = raw_data
        self.stat_data = {}
        self.stat_summary = {}
        self.__process_data(column_group)

    def __process_data(self, column_group):
        grouped = self.raw_data.groupby(column_group)
        all_counts = []

        for product, group_data in grouped:
            count_records = len(group_data)
            self.stat_data[product] = count_records
            all_counts.append(count_records)

        all_data_df = pd.DataFrame(all_counts, columns=['counts'])
        mean_val = all_data_df['counts'].mean()
        median_val = all_data_df['counts'].median()
        mode_val = all_data_df['counts'].mode().iloc[0] if not all_data_df['counts'].mode().empty else None
        variance_val = all_data_df['counts'].var(ddof=1)

        mean_val = round(mean_val, 2)
        median_val = round(median_val, 2)
        mode_val = round(mode_val, 2) if mode_val is not None else None
        variance_val = round(variance_val, 2)

        self.stat_summary = {
            'średnia': mean_val,
            'mediana': median_val,
            'moda': mode_val,
            'wariancja': variance_val
        }




if __name__ == "__main__":
    data1 = {
        'Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego на lpt': ['Produkt A',
                                                                                                  'Produkt A',
                                                                                                  'Produkt B',
                                                                                                  'Produkt B',
                                                                                                  'Produkt B'],
        'Województwo': ['Region 1', 'Region 2', 'Region 1', 'Region 2', 'Region 3']
    }
    df1 = pd.DataFrame(data1)
    processor1 = GeneralDataProcessor(df1,
                                      'Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego на lpt')

    data2 = {
        'Rodzaj produktu rolnego, środка spożywczego lub napoju spirytusowego wpisanego на lpt': ['Produkt C',
                                                                                                  'Produkt C',
                                                                                                  'Produkt D',
                                                                                                  'Produkt D',
                                                                                                  'Produkt D'],
        'Województwo': ['Region 1', 'Region 3', 'Region 2', 'Region 2', 'Region 3']
    }
    df2 = pd.DataFrame(data2)
    processor2 = GeneralDataProcessor(df2,
                                      'Rodzaj produktu rolnego, środка spożywczego lub napoju spirytusowego wpisanego на lpt')

    root = tk.Tk()
    root.title("Диаграммы")

    frame = HistogramFrame(root, processor1, processor2)
    frame.pack(side="top", fill="both", expand=True)

    root.mainloop()
