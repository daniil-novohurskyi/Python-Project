from tkinter import Tk, Frame, Label, Button, Entry, LEFT, RIGHT
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataAnalysisGUI:
    def __init__(self, root, analysis):
        self.root = root
        self.analysis = analysis
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack()

        self.label_start_date = Label(self.frame, text="Start Date (YYYY-MM-DD):")
        self.label_start_date.grid(row=0, column=0)
        self.entry_start_date = Entry(self.frame)
        self.entry_start_date.grid(row=0, column=1)

        self.label_end_date = Label(self.frame, text="End Date (YYYY-MM-DD):")
        self.label_end_date.grid(row=1, column=0)
        self.entry_end_date = Entry(self.frame)
        self.entry_end_date.grid(row=1, column=1)

        self.button_filter = Button(self.frame, text="Filter and Plot", command=self.filter_and_plot)
        self.button_filter.grid(row=2, columnspan=2)

        self.plot_frame = Frame(self.root)
        self.plot_frame.pack()

    def filter_and_plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        filtered_data = self.analysis.filter_data(start_date, end_date)

        fig_bar = self.analysis.plot_bar(filtered_data)
        canvas_bar = FigureCanvasTkAgg(fig_bar, master=self.plot_frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().pack(side=LEFT, fill="both", expand=True)

        fig_line = self.analysis.plot_line(filtered_data)
        canvas_line = FigureCanvasTkAgg(fig_line, master=self.plot_frame)
        canvas_line.draw()
        canvas_line.get_tk_widget().pack(side=RIGHT, fill="both", expand=True)