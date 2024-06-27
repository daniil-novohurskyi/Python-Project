import tkinter as tk
from tkinter import ttk
import pandas as pd

class DataFrameViewer(ttk.Frame):
    def __init__(self, parent, dataframe):
        super().__init__(parent)
        self.dataframe = dataframe
        self.sort_column = None
        self.sort_reverse = False

        self.create_widgets()

    def create_widgets(self):
        # Создаем фрейм для отображения таблицы
        self.frame = ttk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.dataframe = self.dataframe.drop("Year", axis=1)

        # Создаем таблицу Treeview
        self.tree = ttk.Treeview(self.frame, columns=list(self.dataframe.columns), show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        # Добавляем полосы прокрутки
        yscrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        yscrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=yscrollbar.set)

        # Настройка заголовков столбцов и данных
        for column in self.dataframe.columns:
            self.tree.heading(column, text=column, command=lambda col=column: self.sort_by_column(col))
            self.tree.column(column, width=100, anchor="center")

        # Настройка чередования цветов строк
        self.tree.tag_configure('oddrow', background='lightgray')
        self.tree.tag_configure('evenrow', background='white')

        # Добавляем данные в таблицу
        self.treeview_data = []
        self.update_treeview(self.dataframe)

    def update_treeview(self, dataframe):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Добавляем данные в таблицу
        self.treeview_data = []
        for index, row in dataframe.iterrows():
            tag = 'evenrow' if len(self.treeview_data) % 2 == 0 else 'oddrow'
            self.treeview_data.append(self.tree.insert("", "end", values=list(row), tags=(tag,)))

    def sort_by_column(self, column):
        # Переключение порядка сортировки
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        self.sort_column = column

        # Сортировка данных по выбранному столбцу
        self.dataframe = self.dataframe.sort_values(by=column, ascending=not self.sort_reverse).reset_index(drop=True)

        # Обновление отображения таблицы
        self.update_treeview(self.dataframe)