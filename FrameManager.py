import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from handler.data_handler import process_data, print_data_summary
from handler.file_handler import walk_dir_read
from models.DataAnalysis import DataAnalysis
from models.MapDataProcessor import MapDataProcessor
from models.PieChartDataProcessor import PieChartDataProcessor
from view.DataAnalysisGUI import DataAnalysisGUI
from view.DataFrameViewer import DataFrameViewer
from view.MapFrame import MapFrame
from view.PieChartFrame import PieChartFrame


# Пример основного скрипта с использованием FrameManager

class FrameManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side="bottom", fill="x")

        self.frames = {}

        # Настройка растяжения контейнера
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

    def add_frame(self, frame_class, *args):
        frame = frame_class(self.container, *args)
        self.frames[frame_class] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        button = ttk.Button(self.button_frame, text=frame_class.__name__,
                            command=lambda fc=frame_class: self.show_frame(fc))
        button.pack(side="left", fill="x", expand=True)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


if __name__ == "__main__":
    # Инициализация данных
    from handler.data_handler import process_data, print_data_summary
    from handler.file_handler import walk_dir_read
    from models.DataAnalysis import DataAnalysis
    from models.MapDataProcessor import MapDataProcessor
    from models.PieChartDataProcessor import PieChartDataProcessor
    from view.DataAnalysisGUI import DataAnalysisGUI
    from view.PieChartFrame import PieChartFrame

    start_dir = 'data'
    combined_df = walk_dir_read(start_dir)
    processed_df = process_data(combined_df)
    print_data_summary(processed_df)
    analysis = DataAnalysis(processed_df)

    piechart_processor = PieChartDataProcessor(processed_df)
    data_processor = MapDataProcessor(processed_df)

    app = FrameManager()
    app.title("RegionalProductAnalyzer")
    app.attributes('-fullscreen', False)

    # Добавляем фреймы
    app.add_frame(DataAnalysisGUI, analysis)
    app.add_frame(MapFrame, data_processor)
    app.add_frame(PieChartFrame, piechart_processor)
    app.add_frame(DataFrameViewer,processed_df)

    # Показываем начальный фрейм
    app.show_frame(DataFrameViewer)

    app.mainloop()