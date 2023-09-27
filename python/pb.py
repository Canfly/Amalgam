import sys
import json

def merge_json(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1:
        data1 = json.load(f1)
    with open(file2, 'r', encoding='utf-8') as f2:
        data2 = json.load(f2)

    # Объединяем данные по артикулу
    merged_data = {item['артикул']: item for item in data1}
    for item in data2:
        if item['артикул'] not in merged_data:
            merged_data[item['артикул']] = item

    # Записываем объединенные данные в новый файл
    output_file = 'merged_output.json'
    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(list(merged_data.values()), out_file, ensure_ascii=False, indent=4)

    print(f'Данные объединены и сохранены в {output_file}')

if name == "main":
    if len(sys.argv) != 3:
        print("Использование: python program.py file1.json file2.json")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        merge_json(file1, file2)