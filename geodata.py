import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Загрузите файл GeoJSON (предположим, файл содержит границы регионов Польши)
geojson_path = 'geodata/wojewodztwa-max.geojson'

# Загрузите данные GeoJSON с использованием GeoPandas
gdf = gpd.read_file(geojson_path)

# Проверьте структуру данных и убедитесь, что идентификаторы объектов загружены правильно
print(gdf.head())  # выведите первые несколько строк GeoDataFrame для проверки

# Пример данных статистики, которые мы хотим отобразить на карте
# Предположим, у нас есть идентификаторы объектов в GeoJSON и соответствующие значения статистики
stat_data = {
    1: 10,
    2: 20,
    3: 30,
    # добавьте остальные данные
}

# Выведите доступные идентификаторы для проверки
print(gdf['id'].unique())  # замените 'id' на название колонки с идентификаторами в вашем GeoDataFrame

# Создайте колонку в GeoDataFrame для данных статистики
# Замените 'id' на название колонки с идентификаторами в вашем GeoDataFrame
gdf['stat'] = gdf['id'].map(stat_data)

# Проверьте, что данные статистики правильно сопоставлены
print(gdf[['id', 'stat']].head())

# Определите цвета для каждого значения статистики
def get_color(value):
    if value > 25:
        return 'red'
    elif value > 15:
        return 'orange'
    elif value > 5:
        return 'yellow'
    else:
        return 'green'

# Примените функцию определения цвета
gdf['color'] = gdf['stat'].apply(lambda x: get_color(x) if pd.notnull(x) else 'grey')

# Проверьте распределение цветов
print(gdf[['id', 'stat', 'color']].head())

# Создайте фигуру и оси
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Отобразите данные GeoDataFrame с заданными цветами
gdf.plot(ax=ax, color=gdf['color'])

# Настройте отображение
ax.set_title('Statistical Map of Poland')
ax.set_axis_off()

# Сохраните карту в файл
plt.savefig('poland_statistical_map.png', bbox_inches='tight')
plt.show()
