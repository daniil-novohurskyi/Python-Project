from tkinter import Button, Frame, Toplevel, Label, Entry, messagebox

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataAnalysisGUI:
    def __init__(self, root, analysis):
        self.root = root
        self.analysis = analysis
        self.current_plot = None

        self.frame = Frame(root)
        self.frame.pack()

        self.plot_buttons = Frame(root)
        self.plot_buttons.pack()

        self.bar_button = Button(self.plot_buttons, text="Bar Plot", command=self.select_range_for_bar)
        self.bar_button.pack(side="left")

        self.line_button = Button(self.plot_buttons, text="Line Plot", command=self.select_range_for_line)
        self.line_button.pack(side="left")



    def clear_plot(self):
        if self.current_plot:
            self.current_plot.get_tk_widget().pack_forget()
            self.current_plot = None

    def select_range_for_bar(self):
        self.open_range_selector(self.show_bar_plot)

    def select_range_for_line(self):
        self.open_range_selector(self.show_line_plot)



    def open_range_selector(self, plot_function):
        range_selector = Toplevel(self.root)
        range_selector.title("Select Data Range")

        Label(range_selector, text="Start Date (YYYY-MM-DD HH:MM:SS):").grid(row=0, column=0)
        start_entry = Entry(range_selector)
        start_entry.grid(row=0, column=1)

        Label(range_selector, text="End Date (YYYY-MM-DD HH:MM:SS):").grid(row=1, column=0)
        end_entry = Entry(range_selector)
        end_entry.grid(row=1, column=1)

        def submit_range():
            start_date = start_entry.get()
            end_date = end_entry.get()
            try:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                filtered_data = self.analysis.filter_data(start_date, end_date)
                plot_function(filtered_data)
                range_selector.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid date format or range: {e}")

        Button(range_selector, text="Submit", command=submit_range).grid(row=2, columnspan=2)

    def show_bar_plot(self, filtered_data):
        self.clear_plot()
        fig = self.analysis.plot_bar(filtered_data)
        self.current_plot = FigureCanvasTkAgg(fig, master=self.frame)
        self.current_plot.draw()
        self.current_plot.get_tk_widget().pack()

    def show_line_plot(self, filtered_data):
        self.clear_plot()
        fig = self.analysis.plot_line(filtered_data)
        self.current_plot = FigureCanvasTkAgg(fig, master=self.frame)
        self.current_plot.draw()
        self.current_plot.get_tk_widget().pack()
