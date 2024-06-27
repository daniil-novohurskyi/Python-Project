import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class GeneralDataFrame(ttk.Frame):
    def __init__(self, parent, processor1, processor2):
        super().__init__(parent)
        self.class_name = "Informacje ogólne"

        self.processor1 = processor1
        self.processor2 = processor2

        self.create_widgets()

    def __shrink_labels(self, labels):
        tick_labels = labels
        new_tick_labels = []
        for tick in tick_labels:
            shorter_tick = tick
            splited_tick = tick.split(' ')
            if len(splited_tick) > 4:
                shorter_tick = ' '.join(splited_tick[:4])
            new_tick_labels.append(shorter_tick)
        return new_tick_labels

    def create_widgets(self):
        # Уменьшаем размер диаграммы и добавляем пространство для меток
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Добавляем больше пространства для меток
        plt.subplots_adjust(bottom=0.3)
        tick_labels1 = self.__shrink_labels(self.processor1.stat_data.keys())
        self.ax1.bar(tick_labels1, self.processor1.stat_data.values())
        self.ax1.set_title(self.processor1.statistic_title)
        self.ax1.set_xlabel(self.processor1.type_for_analyse)
        self.ax1.set_ylabel("Ilosc rekordow")
        self.ax1.set_xticklabels(tick_labels1, rotation=90, fontsize=7)
        tick_labels2 = self.__shrink_labels(self.processor2.stat_data.keys())
        self.ax2.bar(tick_labels2, self.processor2.stat_data.values())
        self.ax2.set_title(self.processor2.statistic_title)
        self.ax2.set_xlabel(self.processor2.type_for_analyse)
        self.ax2.set_ylabel("Ilosc rekordow")
        self.ax2.set_xticklabels(tick_labels2, rotation=90, fontsize=7)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
