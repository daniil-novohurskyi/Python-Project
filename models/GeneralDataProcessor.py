import pandas as pd


class GeneralDataProcessor:
    def __init__(self, raw_data, column_group,statistic_title,type_for_analyse):
        self.raw_data = raw_data
        self.statistic_title = statistic_title
        self.type_for_analyse = type_for_analyse
        self.stat_data = {}
        self.stat_summary = {}
        self.__process_data(column_group)

    def __process_data(self, column_group):
        # Группировка данных по указанному столбцу
        grouped = self.raw_data.groupby(column_group)

        # Переменная для хранения всех данных для вычисления общих статистических данных
        all_counts = []

        # Обработка каждой группы и сбор данных
        for product, group_data in grouped:
            count_records = len(group_data)
            self.stat_data[product] = count_records
            all_counts.append(count_records)
        # Создание DataFrame из всех данных
        all_data_df = pd.DataFrame(all_counts, columns=['counts'])

        # Вычисление статистических данных
        mean_val = all_data_df['counts'].mean()
        median_val = all_data_df['counts'].median()
        mode_val = all_data_df['counts'].mode().iloc[0] if not all_data_df['counts'].mode().empty else None
        variance_val = all_data_df['counts'].var(ddof=1)

        # Округление значений
        mean_val = round(mean_val, 2)
        median_val = round(median_val, 2)
        mode_val = round(mode_val, 2) if mode_val is not None else None
        variance_val = round(variance_val, 2)

        # Сохранение общих статистических данных в словаре
        self.stat_summary = {
            'średnia': mean_val,
            'mediana': median_val,
            'moda': mode_val,
            'wariancja': variance_val
        }
