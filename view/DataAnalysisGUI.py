from tkinter import Tk, Frame, Label, Button, Scale, HORIZONTAL, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataAnalysisGUI(ttk.Frame):
    def __init__(self, parent, analysis, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.analysis = analysis
        self.create_widgets()
        self.plot()

    def create_widgets(self):
        self.frame = ttk.Frame(self)
        self.frame.pack()

        self.label_start_year = ttk.Label(self.frame, text="Start Year:")
        self.label_start_year.grid(row=0, column=0)
        self.scale_start_year = Scale(self.frame, from_=self.analysis.data['Year'].min(),
                                      to=self.analysis.data['Year'].max(), orient=HORIZONTAL)
        self.scale_start_year.grid(row=0, column=1)

        self.label_end_year = ttk.Label(self.frame, text="End Year:")
        self.label_end_year.grid(row=1, column=0)
        self.scale_end_year = Scale(self.frame, from_=self.analysis.data['Year'].min(),
                                    to=self.analysis.data['Year'].max(), orient=HORIZONTAL)
        self.scale_end_year.set(self.analysis.data['Year'].max())
        self.scale_end_year.grid(row=1, column=1)

        self.button_filter = ttk.Button(self.frame, text="Analyse", command=self.plot)
        self.button_filter.grid(row=2, columnspan=2)

        self.plot_frame = ttk.Frame(self)


        self.plot_frame.pack()

    def plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        start_year = self.scale_start_year.get()
        end_year = self.scale_end_year.get()
        filtered_data = self.analysis.get_data_by_date(f"{start_year}-01-01", f"{end_year}-12-31")
        fig_line = self.analysis.plot_line(filtered_data)

        # Adjust the size of the plot
        fig_line.set_size_inches(12, 6)  # Width, Height in inches

        canvas_line = FigureCanvasTkAgg(fig_line, master=self.plot_frame)
        canvas_line.draw()
        canvas_line.get_tk_widget().pack(side="top", fill="both", expand=True)