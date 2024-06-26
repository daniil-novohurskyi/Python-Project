from tkinter import Tk

from models.DataAnalysis import DataAnalysis
from models.MapDataProcessor import MapDataProcessor
from models.PieChartDataProcessor import PieChartDataProcessor
from view.DataAnalysisGUI import DataAnalysisGUI
from handler.data_handler import process_data, print_data_summary
from handler.file_handler import walk_dir_read
from view.PieChartFrame import PieChartFrame

if __name__ == "__main__":
    start_dir = 'data'
    combined_df = walk_dir_read(start_dir)
    processed_df = process_data(combined_df)
    # print_data_summary(combined_df)
    print_data_summary(processed_df)
    analysis = DataAnalysis(processed_df)
    root = Tk()

    piechart_processor = PieChartDataProcessor(processed_df)
    piechart_GUI = PieChartFrame(root, piechart_processor)
    piechart_GUI.run()
    map_processor = MapDataProcessor(processed_df)
    test_app = MapGUI(root, map_processor)
    test_app.run()

    # app = StatisticsMapApp(root, processed_df)
    # app.run()

    root = Tk()
    root.title("RegionalProductAnalyzer")
    root.attributes('-fullscreen', True)
    app = DataAnalysisGUI(root, analysis)
    root.mainloop()
