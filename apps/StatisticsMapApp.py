import tkinter as tk
from tkinter import ttk

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StatisticsMapApp:

    def __init__(self, root, raw_data):
        self.root = root
        self.root.title("Reprezentacja ilości produktów w województwach")

        # Фрейм для отображения плота и статистики
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Фрейм для отображения плота
        self.plot_frame = tk.Frame(self.main_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Фрейм для отображения статистики
        self.stats_frame = tk.Frame(self.main_frame)
        self.stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))  # Уменьшил ширину, чтобы не заслонять plot_frame

        # Загрузка данных GeoJSON (замените на свой путь к файлу)
        self.geojson_path = '../geodata/wojewodztwa-max.geojson'
        self.gdf = gpd.read_file(self.geojson_path)

        # Пример данных статистики для разных классов по названиям
        self.__make_classes_for_stat_data(raw_data)
        self.stats = self
        # Создание выпадающего списка для выбора класса данных
        self.class_selector = ttk.Combobox(self.root, values=list(self.stat_data.keys()))
        self.class_selector.set(next(iter(self.stat_data.keys())))
        self.class_selector.pack(pady=10)
        self.class_selector.bind("<<ComboboxSelected>>", self.update_plot)

        # Инициализация и отображение начального плота и статистики
        self.create_plot(self.class_selector.get())
        self.display_statistics(self.class_selector.get())

    def __make_classes_for_stat_data(self, raw_data):
        stat_data = {}
        stat_summary = {}
        grouped = raw_data.groupby(
            'Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt')
        for product, group_data in grouped:
            # Создание словаря с количеством продуктов по областям для текущего продукта
            region_counts = group_data['Województwo'].value_counts().to_dict()

            # Добавление словаря для текущего продукта в основной словарь
            stat_data[product] = region_counts

            # Создание DataFrame из словаря region_counts
            region_counts_df = pd.DataFrame.from_dict(region_counts, orient='index', columns=['counts'])

            # Вычисление статистических данных
            mean_val = region_counts_df['counts'].mean()
            median_val = region_counts_df['counts'].median()
            mode_val = region_counts_df['counts'].mode()[0] if not region_counts_df['counts'].mode().empty else None
            variance_val = region_counts_df['counts'].var(ddof=1)

            # Сохранение статистических данных в словаре
            stat_summary[product] = {
                'średnia': mean_val,
                'mediana': median_val,
                'moda': mode_val,
                'wariancja': variance_val
            }

        self.stat_data = stat_data
        self.stat_summary = stat_summary


    def create_plot(self, stat_class):
        # Очистка plot_frame перед добавлением нового плота
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Создание столбца с данными статистики
        self.gdf['stat'] = self.gdf['nazwa'].apply(lambda x: self.stat_data[stat_class].get(x, 0))

        # Создание и отображение плота с использованием matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        self.gdf.plot(ax=ax, column='stat', cmap='YlOrRd', legend=True, legend_kwds={'label': f'Ilosc rekordow '})
        ax.set_title(f'{stat_class}')
        plt.tight_layout()

        # Вставка плота matplotlib в tk.Frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Сохраняем ссылку на объект canvas, чтобы иметь возможность обновлять его
        self.canvas = canvas

    def display_statistics(self, stat_class):
        # Очистка stats_frame перед добавлением новой статистики
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Добавление текстовых данных (медиана, мода, среднее значение)
        stat_values = self.stat_data[stat_class]
        stat_summary = self.stat_summary[stat_class]
        text_data = f"{stat_class}: \n"
        text_data += "\n".join([f"{key}: {value}" for key, value in stat_values.items()])+"\n\n"
        text_data += "Podsumowanie statystyczne:\n\n"
        text_data += "\n\n".join([f"{key}: {value}" for key, value in stat_summary.items()])


        label = tk.Label(self.stats_frame, text=text_data, justify=tk.LEFT, padx=10, pady=10)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_plot(self, event):
        selected_class = self.class_selector.get()
        self.create_plot(selected_class)
        self.display_statistics(selected_class)

    def run(self):
        # Запуск основного цикла tkinter
        self.root.mainloop()

