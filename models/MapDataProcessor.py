import pandas as pd


class MapDataProcessor:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.stat_data = {}
        self.stat_summary = {}
        self.__process_data()

    def __process_data(self):
        grouped = self.raw_data.groupby(
            'Rodzaj produktu rolnego, środka spożywczego lub napoju spirytusowego wpisanego na lpt')
        for product, group_data in grouped:
            # Создание словаря с количеством продуктов по областям для текущего продукта
            region_counts = group_data['Województwo'].value_counts().to_dict()

            # Добавление словаря для текущего продукта в основной словарь
            self.stat_data[product] = region_counts

            # Создание DataFrame из словаря region_counts
            region_counts_df = pd.DataFrame.from_dict(region_counts, orient='index', columns=['counts'])

            # Вычисление статистических данных
            mean_val = region_counts_df['counts'].mean()
            median_val = region_counts_df['counts'].median()
            mode_val = region_counts_df['counts'].mode()[0] if not region_counts_df['counts'].mode().empty else None
            variance_val = region_counts_df['counts'].var(ddof=1)

            # Сохранение статистических данных в словаре
            self.stat_summary[product] = {
                'średnia': mean_val,
                'mediana': median_val,
                'moda': mode_val,
                'wariancja': variance_val
            }