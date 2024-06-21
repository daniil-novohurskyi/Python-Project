import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysis:
    def __init__(self, dataframe):
        self.data = dataframe
        self.clean_data()

    def clean_data(self):
        self.data.columns = self.data.columns.str.replace('\n', '').str.strip()
        self.data['Data wpisu na lpt'] = pd.to_datetime(self.data['Data wpisu na lpt'], errors='coerce')

    def filter_data(self, start_date, end_date):
        filtered_data = self.data[
            (self.data['Data wpisu na lpt'] >= start_date) & (self.data['Data wpisu na lpt'] <= end_date)
        ]
        return filtered_data

    def plot_bar(self, data):
        fig, ax = plt.subplots(figsize=(10, 6))
        data['Year'] = data['Data wpisu na lpt'].dt.year
        sns.countplot(x='Year', data=data, palette='viridis', ax=ax)
        ax.set_title('Количество записей по годам')
        ax.set_xlabel('Год')
        ax.set_ylabel('Количество записей')
        plt.xticks(rotation=45)
        return fig

    def plot_line(self, data):
        fig, ax = plt.subplots(figsize=(10, 6))
        data['Year'] = data['Data wpisu na lpt'].dt.year
        data_grouped = data.groupby('Year').size().reset_index(name='Count')
        sns.lineplot(x='Year', y='Count', data=data_grouped, marker='o', ax=ax)
        ax.set_title('Тренд количества записей по годам')
        ax.set_xlabel('Год')
        ax.set_ylabel('Количество записей')
        plt.xticks(rotation=45)
        return fig
