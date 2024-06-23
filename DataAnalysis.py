import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class DataAnalysis:
    def __init__(self, dataframe):
        self.data = dataframe
        self.clean_data()   # don't touch

    def clean_data(self):
        self.data.columns = self.data.columns.str.replace('\n', '').str.strip()
        self.data['Data wpisu na lpt'] = pd.to_datetime(self.data['Data wpisu na lpt'], errors='coerce')
        self.data['Year'] = self.data['Data wpisu na lpt'].dt.year

    def get_data_by_date(self, start_date, end_date):
        filtered_data = self.data[
            (self.data['Data wpisu na lpt'] >= start_date) & (self.data['Data wpisu na lpt'] <= end_date)
            ]
        return filtered_data

    def get_product_types(self):
        return self.data[
            'Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt'].unique()

    def get_provinces(self):
        return self.data[
            'Województwo'].unique()

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
