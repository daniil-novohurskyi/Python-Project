import tkinter as tk
from tkinter import ttk
import pandas as pd

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
        # Создаем фрейм для отображения таблицы и полосы прокрутки
        self.frame = ttk.Frame(self)
        self.frame.pack(fill="both", expand=True)

        self.dataframe = self.dataframe.drop("Year", axis=1)

        # Вычисляем высоту полосы прокрутки
        scrollbar_height = 30

        # Создаем фрейм для таблицы
        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.grid(row=0, column=0, sticky="nsew")

        # Создаем таблицу Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=list(self.dataframe.columns), show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        # Настройка заголовков столбцов и данных
        for column in self.dataframe.columns:
            self.tree.heading(column, text=column, command=lambda col=column: self.sort_by_column(col))
            self.tree.column(column, width=100, anchor="center")  # Установите ширину столбцов по вашему усмотрению

        # Настройка чередования цветов строк
        self.tree.tag_configure('oddrow', background='lightgray')
        self.tree.tag_configure('evenrow', background='white')

        # Добавляем данные в таблицу
        self.treeview_data = []
        self.update_treeview(self.dataframe)

        # Добавляем полосу прокрутки
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Настройка свойств полосы прокрутки и таблицы
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Установка весов для растяжения столбцов и строк
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

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