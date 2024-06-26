from tkinter import Tk

from models.DataAnalysis import DataAnalysis
from view.DataAnalysisGUI import DataAnalysisGUI
from view.MapGUI import MapDataProcessor
from handler.data_handler import process_data, print_data_summary
from handler.file_handler import walk_dir_read

if __name__ == "__main__":
    start_dir = 'data'
    combined_df = walk_dir_read(start_dir)
    processed_df = process_data(combined_df)
    # print_data_summary(combined_df)
    print_data_summary(processed_df)
    analysis = DataAnalysis(processed_df)
    root = Tk()

    piechart_processor = PieChart.PieChartDataProcessor(processed_df)
    piechart_GUI = PieChart.PieChartGUI(root, piechart_processor)
    piechart_GUI.run()
    data_processor = MapDataProcessor(processed_df)
    test_app = Test.MapGUI(root, data_processor)
    test_app.run()

    # app = StatisticsMapApp(root, processed_df)
    # app.run()

    root = Tk()
    root.title("RegionalProductAnalyzer")
    root.attributes('-fullscreen', True)
    app = DataAnalysisGUI(root, analysis)
    root.mainloop()
