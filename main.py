import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных из CSV файла
file_path = 'Dane_z_mandatów_karnych.csv'
data = pd.read_csv(file_path)

# Преобразование данных: удаление пробелов и переносов строк в названиях столбцов
data.columns = data.columns.str.replace('\n', '').str.strip()

# Просмотр очищенных названий столбцов
print("Очищенные названия столбцов:", data.columns)

# Преобразование числовых данных в формат int
data['Ilość mandatów(w tys.)'] = data['Ilość mandatów(w tys.)'].astype(int)
data['Kwota mandatów(w tys. zł)'] = data['Kwota mandatów(w tys. zł)'].astype(int)

# Добавление фиктивной переменной 'Категория' для обхода предупреждения
data['Категория'] = 'Всего'

# Просмотр первых строк данных
print(data.head())

# Построение гистограммы для количества штрафов по месяцам
plt.figure(figsize=(10, 6))
sns.barplot(x='Miesiąc', y='Ilość mandatów(w tys.)', hue='Категория', data=data, palette='viridis', dodge=False, legend=False)
plt.title('Количество штрафов по месяцам в 2023 году')
plt.xlabel('Месяц')
plt.ylabel('Количество штрафов (тыс.)')
plt.xticks(rotation=45)
plt.show()

# Построение линейного графика для суммы штрафов по месяцам
plt.figure(figsize=(10, 6))
sns.lineplot(x='Miesiąc', y='Kwota mandatów(w tys. zł)', data=data, marker='o', color='b')
plt.title('Сумма штрафов по месяцам в 2023 году')
plt.xlabel('Месяц')
plt.ylabel('Сумма штрафов (тыс. zł)')
plt.xticks(rotation=45)
plt.show()

# Построение тепловой карты корреляции (исключая столбец 'Miesiąc')
plt.figure(figsize=(8, 6))
correlation_matrix = data.drop(columns=['Miesiąc', 'Категория']).corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Тепловая карта корреляции')
plt.show()
