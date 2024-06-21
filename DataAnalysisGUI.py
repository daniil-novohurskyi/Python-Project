from tkinter import Button, Frame

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

        self.bar_button = Button(self.plot_buttons, text="Bar Plot", command=self.show_bar_plot)
        self.bar_button.pack(side="left")

        self.line_button = Button(self.plot_buttons, text="Line Plot", command=self.show_line_plot)
        self.line_button.pack(side="left")

        self.heatmap_button = Button(self.plot_buttons, text="Heatmap", command=self.show_heatmap)
        self.heatmap_button.pack(side="left")

    def clear_plot(self):
        if self.current_plot:
            self.current_plot.get_tk_widget().pack_forget()
            self.current_plot = None

    def show_bar_plot(self):
        self.clear_plot()
        fig = self.analysis.plot_bar()
        self.current_plot = FigureCanvasTkAgg(fig, master=self.frame)
        self.current_plot.draw()
        self.current_plot.get_tk_widget().pack()

    def show_line_plot(self):
        self.clear_plot()
        fig = self.analysis.plot_line()
        self.current_plot = FigureCanvasTkAgg(fig, master=self.frame)
        self.current_plot.draw()
        self.current_plot.get_tk_widget().pack()

    def show_heatmap(self):
        self.clear_plot()
        fig = self.analysis.plot_heatmap()
        self.current_plot = FigureCanvasTkAgg(fig, master=self.frame)
        self.current_plot.draw()
        self.current_plot.get_tk_widget().pack()
