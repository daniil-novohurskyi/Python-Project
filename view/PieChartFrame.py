import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models.PieChartDataProcessor import PieChartDataProcessor

class PieChartFrame(ttk.Frame):
    def __init__(self, parent, data_processor, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.data_processor = data_processor

        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))

        # Frame для отображения плота
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 10))

        # Frame для отображения статистики
        self.stats_frame = ttk.Frame(self.main_frame)
        self.stats_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 10))

        self.class_selector = ttk.Combobox(self, state="readonly", values=list(self.data_processor.stat_data.keys()),
                                           font=("Helvetica 16 bold", 12))
        self.class_selector.set(next(iter(self.data_processor.stat_data.keys())))
        self.class_selector.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 10), padx=(10, 10))
        self.class_selector.bind("<<ComboboxSelected>>", self.update_pie_chart)

        self.create_pie_chart(self.class_selector.get())
        self.display_statistics(self.class_selector.get())

        # Настройка растяжения фреймов
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
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        product_counts = self.data_processor.stat_data[region]

        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, _, autotexts = ax.pie(product_counts.values(), labels=None, autopct='%1.1f%%', startangle=90,
                                      pctdistance=1.075)
        ax.axis('equal')
        ax.set_title(f'Соотношение продуктов в {region}')

        ax.legend(wedges, product_counts.keys(), title="Продукты", loc="lower left", bbox_to_anchor=(-0.155, -0.15),
                  fontsize='small')

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.canvas = canvas

    def display_statistics(self, stat_class):
        # Очистка stats_frame перед добавлением новой статистики
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Добавление текстовых данных (медиана, мода, среднее значение)
        stat_values = self.data_processor.stat_data[stat_class]
        stat_summary = self.data_processor.stat_summary[stat_class]

        data_title = f"Produkty: \n"
        text_data = "\n".join([f"{key}: {value}" for key, value in stat_values.items()]) + "\n"
        summary_title = "Static summary:\n"
        summary_data = "\n".join([f"{key}: {value}" for key, value in stat_summary.items()])

        label_title = tk.Label(self.stats_frame, text=data_title, justify=tk.LEFT, font='Arial 20 bold')
        label_title.pack(anchor="nw")

        label_data = tk.Label(self.stats_frame, text=text_data, justify=tk.LEFT, font='Arial 14')
        label_data.pack(anchor="nw")

        label_summary_title = tk.Label(self.stats_frame, text=summary_title, justify=tk.LEFT, font='Arial 20 bold')
        label_summary_title.pack(anchor="nw")

        label_summary_data = tk.Label(self.stats_frame, text=summary_data, justify=tk.LEFT, font='Arial 14')
        label_summary_data.pack(anchor="nw")

        # Adjust padding to minimize space between labels
        for label in [label_title, label_data, label_summary_title, label_summary_data]:
            label.pack_configure(padx=0, pady=0)

    def update_pie_chart(self, event):
        selected_region = self.class_selector.get()
        self.create_pie_chart(selected_region)
        self.display_statistics(selected_region)
