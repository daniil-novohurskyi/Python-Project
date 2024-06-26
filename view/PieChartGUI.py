import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PieChartGUI:
    def __init__(self, root, data_processor):
        self.root = root
        self.root.title("Соотношение продуктов в воеводствах")

        self.data_processor = data_processor

        # Фрейм для отображения плота и статистики
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Фрейм для отображения плота
        self.plot_frame = tk.Frame(self.main_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Фрейм для отображения статистики
        self.stats_frame = tk.Frame(self.main_frame)
        self.stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))

        # Создание выпадающего списка для выбора региона
        self.region_selector = ttk.Combobox(self.root, values=list(self.data_processor.stat_data.keys()))
        self.region_selector.set(next(iter(self.data_processor.stat_data.keys())))
        self.region_selector.pack(pady=10)
        self.region_selector.bind("<<ComboboxSelected>>", self.update_pie_chart)

        # Инициализация и отображение начального плота и статистики
        self.create_pie_chart(self.region_selector.get())
        self.display_statistics(self.region_selector.get())

    def create_pie_chart(self, region):
        # Очистка plot_frame перед добавлением нового плота
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        product_counts = self.data_processor.stat_data[region]

        # Создание и отображение круговой диаграммы с использованием matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, _, autotexts = ax.pie(product_counts.values(), labels=None, autopct='%1.1f%%', startangle=90,
                                      pctdistance=1.075)
        ax.axis('equal')
        ax.set_title(f'Соотношение продуктов в {region}')

        # Добавление легенды
        ax.legend(wedges, product_counts.keys(), title="Продукты", loc="lower left", bbox_to_anchor=(-0.155, -0.15),
                  fontsize='small')

        # Вставка плота matplotlib в tk.Frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Сохраняем ссылку на объект canvas, чтобы иметь возможность обновлять его
        self.canvas = canvas

    def display_statistics(self, region):
        # Очистка stats_frame перед добавлением новой статистики
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Добавление текстовых данных (медиана, мода, среднее значение)
        product_counts = self.data_processor.stat_data[region]
        stat_summary = self.data_processor.stat_summary.get(region, {})
        text_data = f"Продукты в {region}:\n"
        text_data += "\n".join([f"{key}: {value}" for key, value in product_counts.items()]) + "\n\n"
        text_data += "Подсумок статистики:\n\n"
        text_data += "\n\n".join([f"{key}: {value}" for key, value in stat_summary.items()])

        label = tk.Label(self.stats_frame, text=text_data, justify=tk.LEFT, padx=10, pady=10)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_pie_chart(self, event):
        selected_region = self.region_selector.get()
        self.create_pie_chart(selected_region)
        self.display_statistics(selected_region)

    def run(self):
        self.root.mainloop()


# Создание основного окна tkinter и запуск приложения
if __name__ == "__main__":
    raw_data = pd.read_csv("your_data.csv")  # Замените на ваш файл CSV

    data_processor = PieChartDataProcessor(raw_data)

    root = tk.Tk()
    pie_chart_app = PieChartGUI(root, data_processor)
    pie_chart_app.run()
