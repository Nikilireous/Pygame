from PIL import Image
import math

# Загрузка изображения
image_path = 'Карта.png'  # Укажи путь к изображению
image = Image.open(image_path)
image = image.convert('RGB')

# Словарь для сопоставления базовых цветов с числами
color_mapping = {
    (14, 209, 69): 0,     # Зеленый → Трава
    (86, 91, 87): 1, # Серый → Стена
    (10, 171, 241): 2,     # Синий → Вода
    (255, 127, 39): 3,     # Красный → Лава
    (183, 123, 86): 4        # Черный → Дорога
}

# Порог отклонения для цвета
threshold = 50

# Функция для сравнения цветов с учётом отклонения
def is_similar_color(color1, color2, threshold):
    return all(abs(c1 - c2) <= threshold for c1, c2 in zip(color1, color2))

# Функция для поиска ближайшего цвета
def find_closest_color(pixel, color_mapping, threshold):
    for base_color, value in color_mapping.items():
        if is_similar_color(pixel, base_color, threshold):
            return value
    return -1  # Если цвет не найден, вернуть -1 (или другой код)

# Преобразование изображения в матрицу
width, height = image.size
matrix = []
for y in range(height):
    row = []
    for x in range(width):
        pixel = image.getpixel((x, y))
        closest_value = find_closest_color(pixel, color_mapping, threshold)
        row.append(closest_value)
    matrix.append(row)

# Вывод матрицы
for row in matrix:
    print(row)

# Сохранение матрицы в файл (опционально)
with open('map_matrix.txt', 'w') as file:
    for row in matrix:
        file.write(' '.join(map(str, row)) + '\n')
