import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.PieChartDataProcessor import PieChartDataProcessor


class PieChartFrame(ttk.Frame):
    def __init__(self, parent, data_processor, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.data_processor = data_processor

        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew")

        self.stats_frame = ttk.Frame(self.main_frame)
        self.stats_frame.grid(row=0, column=0, sticky="nsew")

        self.region_selector = ttk.Combobox(self, values=list(self.data_processor.stat_data.keys()))
        self.region_selector.set(next(iter(self.data_processor.stat_data.keys())))
        self.region_selector.grid(row=1, column=0, columnspan=2, pady=10)
        self.region_selector.bind("<<ComboboxSelected>>", self.update_pie_chart)

        self.create_pie_chart(self.region_selector.get())
        self.display_statistics(self.region_selector.get())

    def create_pie_chart(self, region):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        product_counts = self.data_processor.stat_data[region]

        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, _, autotexts = ax.pie(product_counts.values(), labels=None, autopct='%1.1f%%', startangle=90,
                                      pctdistance=1.075)
        ax.axis('equal')
        ax.set_title(f'Соотношение продуктов в {region}')

        ax.legend(wedges, product_counts.keys(), title="Продукты", loc="lower left", bbox_to_anchor=(-0.155, -0.15),
                  fontsize='small')

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.canvas = canvas

    def display_statistics(self, region):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        product_counts = self.data_processor.stat_data[region]
        stat_summary = self.data_processor.stat_summary.get(region, {})
        text_data = f"Продукты в {region}:\n"
        text_data += "\n".join([f"{key}: {value}" for key, value in product_counts.items()]) + "\n\n"
        text_data += "Подсумок статистики:\n\n"
        text_data += "\n\n".join([f"{key}: {value}" for key, value in stat_summary.items()])

        label = tk.Label(self.stats_frame, text=text_data, justify=tk.LEFT, padx=10, pady=10)
        label.grid(row=0, column=0, sticky="nsew")

    def update_pie_chart(self, event):
        selected_region = self.region_selector.get()
        self.create_pie_chart(selected_region)
        self.display_statistics(selected_region)