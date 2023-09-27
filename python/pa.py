import sys
import json

# Проверка наличия аргументов командной строки
if len(sys.argv) < 3:
    print("Необходимо указать два JSON файла для объединения!")
    print("Пример использования: python programm.py file1.json file2.json")
    sys.exit(1)

# Чтение данных из первого файла
file1_name = sys.argv[1]
try:
    with open(file1_name, 'r') as file1:
        data1 = json.load(file1)
except FileNotFoundError:
    print("Файл", file1_name, "не найден.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Файл", file1_name, "не является допустимым JSON-файлом.")
    sys.exit(1)

# Чтение данных из второго файла
file2_name = sys.argv[2]
try:
    with open(file2_name, 'r') as file2:
        data2 = json.load(file2)
except FileNotFoundError:
    print("Файл", file2_name, "не найден.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Файл", file2_name, "не является допустимым JSON-файлом.")
    sys.exit(1)

# Создание словаря для хранения объединенных данных
combined_data = {}

# Объединение данных из первого файла
for item in data1:
    article = item.get('артикул')
    if article in combined_data:
        combined_data[article].append(item)
    else:
        combined_data[article] = [item]

# Объединение данных из второго файла
for item in data2:
    article = item.get('артикул')
    if article in combined_data:
        combined_data[article].append(item)
    else:
        combined_data[article] = [item]

# Преобразование словаря с объединенными данными в список
output_data = []
for article in combined_data:
    items = combined_data[article]
    output_data.extend(items)

# Вывод объединенных данных
print("Объединенные данные:")
for item in output_data:
    print(item)

# Запись объединенных данных в новый файл
output_file_name = "combined.json"
with open(output_file_name, 'w') as output_file:
    json.dump(output_data, output_file, indent=4)

print("Данные сохранены в файл", output_file_name)