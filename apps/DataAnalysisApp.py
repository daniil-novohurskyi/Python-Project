import tkinter as tk
from tkinter import Frame, Label, Button, Scale, HORIZONTAL
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


class DataAnalysisApp:
    def __init__(self, root, dataframe):
        self.root = root
        self.data = dataframe
        self.clean_data()

        self.create_widgets()

    def clean_data(self):
        self.data.columns = self.data.columns.str.replace('\n', '').str.strip()
        self.data['Data wpisu na lpt'] = pd.to_datetime(self.data['Data wpisu na lpt'], errors='coerce')
        self.data['Year'] = self.data['Data wpisu na lpt'].dt.year

    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack()

        self.label_start_year = Label(self.frame, text="Start Year:")
        self.label_start_year.grid(row=0, column=0)
        self.scale_start_year = Scale(self.frame, from_=self.data['Year'].min(),
                                      to=self.data['Year'].max(), orient=HORIZONTAL)
        self.scale_start_year.grid(row=0, column=1)

        self.label_end_year = Label(self.frame, text="End Year:")
        self.label_end_year.grid(row=1, column=0)
        self.scale_end_year = Scale(self.frame, from_=self.data['Year'].min(),
                                    to=self.data['Year'].max(), orient=HORIZONTAL)
        self.scale_end_year.grid(row=1, column=1)

        self.button_filter = Button(self.frame, text="Analyse", command=self.plot)
        self.button_filter.grid(row=2, columnspan=2)

        self.plot_frame = Frame(self.root)
        self.plot_frame.pack()

    def get_data_by_date(self, start_date, end_date):
        filtered_data = self.data[
            (self.data['Data wpisu na lpt'] >= start_date) & (self.data['Data wpisu na lpt'] <= end_date)
            ]
        return filtered_data

    def plot_line(self, data):
        fig, ax = plt.subplots(figsize=(12, 8))
        data_grouped = data.groupby('Year').size().reset_index(name='Count')
        sns.lineplot(x='Year', y='Count', data=data_grouped, marker='o', ax=ax)
        for x, y in zip(data_grouped['Year'], data_grouped['Count']):
            ax.text(x, y, f'{y}', fontsize=12, ha='right')
        ax.set_title('Trend liczby rekordów według roku', fontsize=16)
        ax.set_xlabel('Rok', fontsize=14)
        ax.set_ylabel('Ilość wpisów', fontsize=14)
        ax.grid(True)
        plt.xticks(rotation=45)
        return fig

    def plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        start_year = self.scale_start_year.get()
        end_year = self.scale_end_year.get()
        filtered_data = self.get_data_by_date(f"{start_year}-01-01", f"{end_year}-12-31")
        fig_line = self.plot_line(filtered_data)
        canvas_line = FigureCanvasTkAgg(fig_line, master=self.plot_frame)
        canvas_line.draw()
        canvas_line.get_tk_widget().pack(side="top", fill="both", expand=True)

    def run(self):
        # Запуск основного цикла tkinter
        self.root.mainloop()
