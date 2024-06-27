import tkinter as tk
from tkinter import ttk

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MapFrame(ttk.Frame):
    """
    Frame displaying a map plot and statistics for regional data analysis.

    Attributes:
        data_processor (MapDataProcessor): Instance of MapDataProcessor for data processing.
        main_frame (ttk.Frame): Main frame containing the plot and statistics frames.
        plot_frame (ttk.Frame): Frame for displaying the map plot.
        stats_frame (ttk.Frame): Frame for displaying statistics.
        geojson_path (str): Path to the GeoJSON file with regional boundaries.
        gdf (GeoDataFrame): GeoDataFrame containing the geographical data.

    Methods:
        create_plot(stat_class):
            Generates and displays a choropleth map plot for the selected product category.
        update_plot(event):
            Updates the choropleth map plot based on user selection.
        display_statistics(stat_class):
            Displays statistics for the selected product category.
    """

    def __init__(self, parent, data_processor, *args, **kwargs):
        """
        Initializes the MapFrame instance.

        Args:
            parent (tk.Widget): Parent widget to which this frame belongs.
            data_processor (MapDataProcessor): Instance of MapDataProcessor for data processing.
        """
        super().__init__(parent, *args, **kwargs)
        self.class_name = "Schemat mapy"

        # Store the data processor instance for processing data
        self.canvas = None
        self.data_processor = data_processor

        # Create main frame for layout
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))

        # Frame for displaying the map plot
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 10))

        # Frame for displaying statistics
        self.stats_frame = ttk.Frame(self.main_frame)
        self.stats_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 10))

        # Path to GeoJSON file with regional boundaries
        self.geojson_path = 'resources/wojewodztwa-max.geojson'
        self.gdf = gpd.read_file(self.geojson_path)

        # Combobox for selecting product category
        self.class_selector = ttk.Combobox(self, state="readonly", values=list(self.data_processor.stat_data.keys()),
                                           font=("Helvetica 16 bold", 12))
        self.class_selector.set(next(iter(self.data_processor.stat_data.keys())))
        self.class_selector.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 10), padx=(10, 10))
        self.class_selector.bind("<<ComboboxSelected>>", self.update_plot)

        # Initialize with default plot and statistics
        self.create_plot(self.class_selector.get())
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

    def create_plot(self, stat_class):
        """
        Generates and displays a choropleth map plot for the selected product category.

        Args:
            stat_class (str): The product category for which to generate the plot.
        """
        # Clear previous plot widgets
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Calculate statistics data for each region
        self.gdf['stat'] = self.gdf['nazwa'].apply(lambda x: self.data_processor.stat_data[stat_class].get(x, 0))

        # Create a figure and axis for the plot
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot choropleth map using GeoDataFrame and statistics data
        self.gdf.plot(ax=ax, column='stat', cmap='YlOrRd', legend=True, legend_kwds={'label': 'Ilość rekordów'})

        # Set title for the plot
        ax.set_title(f'{stat_class}')
        plt.tight_layout()

        # Create a Tkinter canvas for embedding matplotlib plot into Tkinter GUI
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Store canvas reference for updating plot
        self.canvas = canvas

    def update_plot(self, event):
        """
        Updates the choropleth map plot based on user selection.

        Args:
            event: The event that triggered the update.
        """
        # Get selected product category from combobox
        selected_class = self.class_selector.get()

        # Recreate plot for the selected product category
        self.create_plot(selected_class)

        # Display statistics for the selected product category
        self.display_statistics(selected_class)

    def display_statistics(self, stat_class):
        """
        Displays statistics for the selected product category.

        Args:
            stat_class (str): The product category for which to display statistics.
        """
        # Clear previous statistics widgets
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Retrieve statistics data and summary for the selected product category
        stat_values = self.data_processor.stat_data[stat_class]
        stat_summary = self.data_processor.stat_summary[stat_class]

        # Format data and summary information
        data_title = f"Produkt: {stat_class}\n"
        text_data = "\n".join([f"{key}: {value}" for key, value in stat_values.items()]) + "\n"
        summary_title = "Podsumowanie statystyk:\n"
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

        for i in range(4):
            self.stats_frame.rowconfigure(i, weight=1)
        self.stats_frame.columnconfigure(0, weight=1)
