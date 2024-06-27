import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PieChartFrame(ttk.Frame):
    """
    Frame displaying a pie chart and statistics for product distribution in regions.

    Attributes:
        data_processor (MapDataProcessor): Instance of MapDataProcessor for data processing.
        main_frame (ttk.Frame): Main frame containing the plot and statistics frames.
        plot_frame (ttk.Frame): Frame for displaying the pie chart.
        stats_frame (ttk.Frame): Frame for displaying statistics.
        class_selector (ttk.Combobox): Combobox for selecting a region to display data for.
        canvas (FigureCanvasTkAgg): Canvas for displaying the pie chart.

    Methods:
        create_pie_chart(region):
            Generates and displays a pie chart for the selected region.
        update_pie_chart(event):
            Updates the pie chart based on user selection.
        display_statistics(stat_class):
            Displays statistics for the selected region.
    """

    def __init__(self, parent, data_processor, *args, **kwargs):
        """
        Initializes the PieChartFrame instance.

        Args:
            parent (tk.Widget): Parent widget to which this frame belongs.
            data_processor (MapDataProcessor): Instance of MapDataProcessor for data processing.
        """
        super().__init__(parent, *args, **kwargs)

        self.canvas = None
        # Store the data processor instance for processing data
        self.data_processor = data_processor

        # Create main frame for layout
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))

        # Frame for displaying the pie chart
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 10))

        # Frame for displaying statistics
        self.stats_frame = ttk.Frame(self.main_frame)
        self.stats_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 10))

        # Combobox for selecting a region
        self.class_selector = ttk.Combobox(self, state="readonly", values=list(self.data_processor.stat_data.keys()),
                                           font=("Helvetica 16 bold", 12))
        self.class_selector.set(next(iter(self.data_processor.stat_data.keys())))
        self.class_selector.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 10), padx=(10, 10))

        # Bind combobox selection event to update pie chart
        self.class_selector.bind("<<ComboboxSelected>>", self.update_pie_chart)

        # Create initial pie chart and display statistics
        self.create_pie_chart(self.class_selector.get())
        self.display_statistics(self.class_selector.get())

        # Configure row and column weights for resizing
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.stats_frame.rowconfigure(0, weight=1)
        self.stats_frame.rowconfigure(1, weight=1)
        self.stats_frame.rowconfigure(2, weight=1)
        self.stats_frame.rowconfigure(3, weight=1)
        self.stats_frame.columnconfigure(0, weight=1)
        self.plot_frame.rowconfigure(0, weight=1)
        self.plot_frame.columnconfigure(0, weight=1)

    def create_pie_chart(self, region):
        """
        Generates and displays a pie chart for the selected region.

        Args:
            region (str): The region for which to generate the pie chart.
        """
        # Clear previous plot widgets
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Retrieve product counts for the selected region
        product_counts = self.data_processor.stat_data[region]

        # Create a figure and axis for the pie chart
        fig, ax = plt.subplots(figsize=(8, 6))

        # Generate pie chart with product counts, formatting labels and percentages
        wedges, _, autotexts = ax.pie(product_counts.values(), labels=None, autopct='%1.1f%%', startangle=90,
                                      pctdistance=1.075)

        # Equal aspect ratio for a perfect circle
        ax.axis('equal')

        # Set title for the pie chart
        ax.set_title(f'Product Distribution in {region}')

        # Add legend with product names
        ax.legend(wedges, product_counts.keys(), title="Products", loc="lower left", bbox_to_anchor=(-0.155, -0.15),
                  fontsize='small')

        # Create a Tkinter canvas for embedding matplotlib plot into Tkinter GUI
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Store canvas reference for updating the plot
        self.canvas = canvas

    def display_statistics(self, stat_class):
        """
        Displays statistics for the selected region.

        Args:
            stat_class (str): The region for which to display statistics.
        """
        # Clear previous statistics widgets
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Retrieve product counts and summary statistics for the selected region
        stat_values = self.data_processor.stat_data[stat_class]
        stat_summary = self.data_processor.stat_summary[stat_class]

        # Format data and summary information
        data_title = f"Products: {stat_class}\n"
        text_data = "\n".join([f"{key}: {value}" for key, value in stat_values.items()]) + "\n"
        summary_title = "Statistics summary:\n"
        summary_data = "\n".join([f"{key}: {value}" for key, value in stat_summary.items()])

        # Create labels for displaying data and summary
        label_title = tk.Label(self.stats_frame, text=data_title, justify=tk.LEFT, font='Arial 20 bold')
        label_title.pack(anchor="nw")

        label_data = tk.Label(self.stats_frame, text=text_data, justify=tk.LEFT, font='Arial 14')
        label_data.pack(anchor="nw")

        label_summary_title = tk.Label(self.stats_frame, text=summary_title, justify=tk.LEFT, font='Arial 20 bold')
        label_summary_title.pack(anchor="nw")

        label_summary_data = tk.Label(self.stats_frame, text=summary_data, justify=tk.LEFT, font='Arial 14')
        label_summary_data.pack(anchor="nw")

        # Configure row and column weights for resizing
        for label in [label_title, label_data, label_summary_title, label_summary_data]:
            label.pack_configure(padx=0, pady=0)

    def update_pie_chart(self, event):
        """
        Updates the pie chart based on user selection.

        Args:
            event: The event that triggered the update.
        """
        # Get selected region from combobox
        selected_region = self.class_selector.get()

        # Recreate pie chart for the selected region
        self.create_pie_chart(selected_region)

        # Display statistics for the selected region
        self.display_statistics(selected_region)
