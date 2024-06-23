from tkinter import Tk, Frame, Label, Button, Scale, HORIZONTAL
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataAnalysisGUI:
    def __init__(self, root, analysis):
        self.root = root
        self.analysis = analysis
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack()

        self.label_start_year = Label(self.frame, text="Start Year:")
        self.label_start_year.grid(row=0, column=0)
        self.scale_start_year = Scale(self.frame, from_=self.analysis.data['Year'].min(),
                                      to=self.analysis.data['Year'].max(), orient=HORIZONTAL)
        self.scale_start_year.grid(row=0, column=1)

        self.label_end_year = Label(self.frame, text="End Year:")
        self.label_end_year.grid(row=1, column=0)
        self.scale_end_year = Scale(self.frame, from_=self.analysis.data['Year'].min(),
                                    to=self.analysis.data['Year'].max(), orient=HORIZONTAL)
        self.scale_end_year.grid(row=1, column=1)

        self.button_filter = Button(self.frame, text="Analyse", command=self.plot)
        self.button_filter.grid(row=2, columnspan=2)

        self.plot_frame = Frame(self.root)
        self.plot_frame.pack()

    def plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        start_year = self.scale_start_year.get()
        end_year = self.scale_end_year.get()
        filtered_data = self.analysis.get_data_by_date(f"{start_year}-01-01", f"{end_year}-12-31")
        fig_line = self.analysis.plot_line(filtered_data)
        canvas_line = FigureCanvasTkAgg(fig_line, master=self.plot_frame)
        canvas_line.draw()
        canvas_line.get_tk_widget().pack(side="top", fill="both", expand=True)