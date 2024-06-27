import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GeneralDataFrame(ttk.Frame):
    """
    A frame for displaying two bar charts side by side using data processors.

    Attributes:
        class_name (str): Name of the class for identification.
        processor1 (DataProcessor): First data processor instance.
        processor2 (DataProcessor): Second data processor instance.
        fig (matplotlib.figure.Figure): Matplotlib figure object for the plot.
        ax1 (matplotlib.axes.Axes): Axes for the first subplot.
        ax2 (matplotlib.axes.Axes): Axes for the second subplot.
        canvas (FigureCanvasTkAgg): Matplotlib canvas widget for displaying the figure.

    Methods:
        __shrink_labels(labels):
            Internal method to shorten tick labels for better display.
        create_widgets():
            Creates and arranges the widgets in the frame, including the bar charts.
    """

    def __init__(self, parent, processor1, processor2):
        """
        Initializes the GeneralDataFrame instance.

        Args:
            parent (tk.Widget): Parent widget to which this frame belongs.
            processor1 (DataProcessor): First data processor instance.
            processor2 (DataProcessor): Second data processor instance.
        """
        super().__init__(parent)
        self.class_name = "Informacje ogólne"  # Class name for identification
        self.processor1 = processor1  # Instance of the first data processor
        self.processor2 = processor2  # Instance of the second data processor
        self.create_widgets()

    def __shrink_labels(self, labels):
        """
        Internal method to shorten tick labels for better display.

        Args:
            labels (list): List of tick labels to be shortened.

        Returns:
            list: List of shortened tick labels.
        """
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
        """
        Creates and arranges the widgets in the frame, including the bar charts.
        """
        # Create subplots for the two processors
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Adjust subplot spacing for better label visibility
        plt.subplots_adjust(bottom=0.3)

        # Plot data for processor1
        tick_labels1 = self.__shrink_labels(list(self.processor1.stat_data.keys()))
        self.ax1.bar(tick_labels1, list(self.processor1.stat_data.values()))
        self.ax1.set_title(self.processor1.statistic_title)
        self.ax1.set_xlabel(self.processor1.type_for_analyse)
        self.ax1.set_ylabel("Ilosc rekordow")
        self.ax1.set_xticklabels(tick_labels1, rotation=90, fontsize=7)

        # Plot data for processor2
        tick_labels2 = self.__shrink_labels(list(self.processor2.stat_data.keys()))
        self.ax2.bar(tick_labels2, list(self.processor2.stat_data.values()))
        self.ax2.set_title(self.processor2.statistic_title)
        self.ax2.set_xlabel(self.processor2.type_for_analyse)
        self.ax2.set_ylabel("Ilosc rekordow")
        self.ax2.set_xticklabels(tick_labels2, rotation=90, fontsize=7)

        # Embed the plot into a Tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
