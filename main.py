from services.FrameManager import FrameManager
from view.TableFrame import TableFrame
from view.MapFrame import MapFrame
from handlers.DataHandler import process_data, print_data_summary
from handlers.FileHandler import walk_dir_read
from models.PlotProcessor import PlotProcessor
from models.MapDataProcessor import MapDataProcessor
from models.PieChartDataProcessor import PieChartDataProcessor
from view.PlotFrame import PlotFrame
from view.PieChartFrame import PieChartFrame

if __name__ == "__main__":
    """
    Main entry point for the Regional Product Analyzer application.

    This script initializes the application by reading and processing data from
    CSV files, performing analysis, and launching a GUI to visualize the data.
    """
    # Set the starting directory for reading data
    start_dir = 'data'
    # Read all CSV files from the specified directory and combine them into one DataFrame
    combined_df = walk_dir_read(start_dir)
    # Process the combined DataFrame for further analysis
    processed_df = process_data(combined_df)
    # Print a summary of the data in console (for verification)
    print_data_summary(processed_df)

    # Create data processors for different types of visualizations
    plot_processor = PlotProcessor(processed_df)
    pie_chart_processor = PieChartDataProcessor(processed_df)
    data_processor = MapDataProcessor(processed_df)

    # Create the main application with a frame manager
    app = FrameManager()
    app.title("Regional Product Analyzer")
    app.attributes('-fullscreen', False)

    # Add frames with different visualizations to the application
    app.add_frame(PlotFrame, plot_processor)  # Frame for tables
    app.add_frame(MapFrame, data_processor)  # Frame for maps
    app.add_frame(PieChartFrame, pie_chart_processor)  # Frame for pie chart
    app.add_frame(TableFrame, processed_df)  # Frame for table

    # Show the initial frame when the application starts
    app.show_frame(PlotFrame)

    # Run the main loop of the application
    app.mainloop()
