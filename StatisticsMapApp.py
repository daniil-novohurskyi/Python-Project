import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class StatisticsMapApp:

    def __init__(self, root, raw_data):
        self.root = root
        self.root.title("Отображение плотов по классам данных")

        # Фрейм для отображения плота
        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Загрузка данных GeoJSON (замените на свой путь к файлу)
        self.geojson_path = 'geodata/wojewodztwa-max.geojson'
        self.gdf = gpd.read_file(self.geojson_path)

        # Пример данных статистики для разных классов по названиям
        self.stat_data = self.__make_classes_for_stat_data(raw_data)

        # Создание выпадающего списка для выбора класса данных
        self.class_selector = ttk.Combobox(self.root, values=list(self.stat_data.keys()))
        self.class_selector.set(next(iter(self.stat_data.keys())))
        self.class_selector.pack(pady=10)
        self.class_selector.bind("<<ComboboxSelected>>", self.update_plot)

        # Инициализация и отображение начального плота
        self.create_plot(self.class_selector.get())

    def __make_classes_for_stat_data(self,raw_data):
        stat_data = {}
        grouped = raw_data.groupby(
            'Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt')
        for product, group_data in grouped:
            # Создание словаря с количеством продуктов по областям для текущего продукта
            region_counts = group_data['Województwo'].value_counts().to_dict()

            # Добавление словаря для текущего продукта в основной словарь
            stat_data[product] = region_counts
        return stat_data

    def create_plot(self, stat_class):
        # Очистка plot_frame перед добавлением нового плота
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Создание столбца с данными статистики
        self.gdf['stat'] = self.gdf['nazwa'].apply(lambda x: self.stat_data[stat_class].get(x, 0))

        # Создание и отображение плота с использованием matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        self.gdf.plot(ax=ax, column='stat', cmap='YlOrRd', legend=True, legend_kwds={'label': f'Statistics for {stat_class}'})
        ax.set_title(f'Statistics Map: {stat_class}')
        plt.tight_layout()

        # Вставка плота matplotlib в tk.Frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Сохраняем ссылку на объект canvas, чтобы иметь возможность обновлять его
        self.canvas = canvas

    def update_plot(self, event):
        selected_class = self.class_selector.get()
        self.create_plot(selected_class)

    def run(self):
        # Запуск основного цикла tkinter
        self.root.mainloop()

# Создание основного окна tkinter и запуск приложения

