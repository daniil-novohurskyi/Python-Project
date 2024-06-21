import pandas as pd
import matplotlib.pyplot as plt
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

    def show_data(self):
        print("Очищенные названия столбцов:", self.data.columns)
        print(self.data.head())

    def plot_bar(self):
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Miesiąc', y='Ilość mandatów(w tys.)', hue='Категория', data=self.data, palette='viridis',
                    dodge=False, legend=False)
        plt.title('Количество штрафов по месяцам в 2023 году')
        plt.xlabel('Месяц')
        plt.ylabel('Количество штрафов (тыс.)')
        plt.xticks(rotation=45)
        plt.show()

    def plot_line(self):
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='Miesiąc', y='Kwota mandatów(w tys. zł)', data=self.data, marker='o', color='b')
        plt.title('Сумма штрафов по месяцам в 2023 году')
        plt.xlabel('Месяц')
        plt.ylabel('Сумма штрафов (тыс. zł)')
        plt.xticks(rotation=45)
        plt.show()

    def plot_heatmap(self):
        plt.figure(figsize=(8, 6))
        correlation_matrix = self.data.drop(columns=['Miesiąc', 'Категория']).corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Тепловая карта корреляции')
        plt.show()


if __name__ == "__main__":
    file_path = 'Dane_z_mandatów_karnych.csv'
    analysis = DataAnalysis(file_path)
    analysis.show_data()
    analysis.plot_bar()
    analysis.plot_line()
    analysis.plot_heatmap()
