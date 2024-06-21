import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class DataAnalysis:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.load_data()
        self.clean_data()
        self.add_dummy_category()

    def load_data(self):
        self.data = pd.read_csv(self.file_path)

    def clean_data(self):
        self.data.columns = self.data.columns.str.replace('\n', '').str.strip()
        self.data['Ilość mandatów(w tys.)'] = self.data['Ilość mandatów(w tys.)'].astype(int)
        self.data['Kwota mandatów(w tys. zł)'] = self.data['Kwota mandatów(w tys. zł)'].astype(int)

    def add_dummy_category(self):
        self.data['Категория'] = 'Всего'

    def plot_bar(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Miesiąc', y='Ilość mandatów(w tys.)', hue='Категория', data=self.data, palette='viridis',
                    dodge=False, legend=False, ax=ax)
        ax.set_title('Количество штрафов по месяцам в 2023 году')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Количество штрафов (тыс.)')
        ax.set_xticks(range(len(self.data['Miesiąc'].unique())))
        ax.set_xticklabels(self.data['Miesiąc'].unique(), rotation=45)
        return fig

    def plot_line(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='Miesiąc', y='Kwota mandatów(w tys. zł)', data=self.data, marker='o', color='b', ax=ax)
        ax.set_title('Сумма штрафов по месяцам в 2023 году')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Сумма штрафов (тыс. zł)')
        ax.set_xticks(range(len(self.data['Miesiąc'].unique())))
        ax.set_xticklabels(self.data['Miesiąc'].unique(), rotation=45)
        return fig

    def plot_heatmap(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        correlation_matrix = self.data.drop(columns=['Miesiąc', 'Категория']).corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
        ax.set_title('Тепловая карта корреляции')
        return fig
