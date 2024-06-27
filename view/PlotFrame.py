from tkinter import Scale, HORIZONTAL, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns


def create_plot(data):
    """
    Creates a line plot showing the trend of record counts by year.

    Args:
        data (DataFrame): The data to plot, containing at least 'Year' column.

    Returns:
        Figure: The matplotlib figure object containing the plot.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    # Group data by 'Year' and count records
    data_grouped = data.groupby('Year').size().reset_index(name='Count')
    # Create a line plot with markers
    sns.lineplot(x='Year', y='Count', data=data_grouped, marker='o', ax=ax)
    # Display count values as text on the plot
    for x, y in zip(data_grouped['Year'], data_grouped['Count']):
        ax.text(x, y, f'{y}', fontsize=12, ha='right')
    # Set plot title and labels
    ax.set_title('Trend liczby rekordów według roku', fontsize=16)
    ax.set_xlabel('')
    ax.set_ylabel('Ilość rekordów', fontsize=14)
    ax.grid(True)
    plt.xticks(rotation=45)
    return fig


class PlotFrame(ttk.Frame):
    """
    A Tkinter frame for displaying a plot with a filter to select the date range.

    Attributes:
        analysis (Analysis): The analysis object containing the data and methods to process it.
        frame (ttk.Frame): The main frame containing the widgets.
        label_start_year (ttk.Label): The label for the start year scale.
        scale_start_year (Scale): The scale widget for selecting the start year.
        label_end_year (ttk.Label): The label for the end year scale.
        scale_end_year (Scale): The scale widget for selecting the end year.
        button_filter (ttk.Button): The button to trigger the plot update.
        plot_frame (ttk.Frame): The frame for displaying the plot.

    Methods:
        create_widgets():
            Creates and arranges the widgets in the frame.
        display_plot():
            Displays the plot based on the selected date range.
    """

    def __init__(self, parent, analysis, *args, **kwargs):
        """
        Initializes the PlotFrame instance.

        Args:
            parent (tk.Widget): The parent widget to which this frame belongs.
            analysis (Analysis): The analysis object containing the data and methods to process it.
        """
        super().__init__(parent, *args, **kwargs)
        # Initialize attributes for widgets and data
        self.plot_frame = None
        self.button_filter = None
        self.scale_end_year = None
        self.scale_start_year = None
        self.label_end_year = None
        self.label_start_year = None
        self.frame = None
        self.analysis = analysis
        self.create_widgets()
        self.display_plot()

    def create_widgets(self):
        """
        Creates and arranges the widgets in the frame.
        """
        # Create a main frame for layout
        self.frame = ttk.Frame(self)
        self.frame.pack()

        # Label and Scale widget for selecting start year
        self.label_start_year = ttk.Label(self.frame, text="Start Year:")
        self.label_start_year.grid(row=0, column=0)
        self.scale_start_year = Scale(self.frame, from_=self.analysis.data['Year'].min(),
                                      to=self.analysis.data['Year'].max(), orient=HORIZONTAL)
        self.scale_start_year.grid(row=0, column=1)

        # Label and Scale widget for selecting end year
        self.label_end_year = ttk.Label(self.frame, text="End Year:")
        self.label_end_year.grid(row=1, column=0)
        self.scale_end_year = Scale(self.frame, from_=self.analysis.data['Year'].min(),
                                    to=self.analysis.data['Year'].max(), orient=HORIZONTAL)
        self.scale_end_year.set(self.analysis.data['Year'].max())  # Set default to max year
        self.scale_end_year.grid(row=1, column=1)

        # Button to trigger plot update
        self.button_filter = ttk.Button(self.frame, text="OK", command=self.display_plot)
        self.button_filter.grid(row=2, columnspan=2)

        # Frame for displaying the plot
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack()

    def display_plot(self):
        """
        Displays the plot based on the selected date range.
        """
        # Clear previous plot widgets
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Get selected start and end years from scales
        start_year = self.scale_start_year.get()
        end_year = self.scale_end_year.get()

        # Filter data based on selected date range
        filtered_data = self.analysis.get_data_by_date(f"{start_year}-01-01", f"{end_year}-12-31")

        # Create a line plot with filtered data
        fig_line = create_plot(filtered_data)

        # Adjust the size of the plot
        fig_line.set_size_inches(12, 6)  # Width, Height in inches

        # Embed the matplotlib plot into Tkinter canvas
        canvas_line = FigureCanvasTkAgg(fig_line, master=self.plot_frame)
        canvas_line.draw()
        canvas_line.get_tk_widget().pack(side="top", fill="both", expand=True)
