import os
import re
import csv
import yaml
import json
import chardet


"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().

2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.

3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

# 1.


def get_encoding(file):
    with open(file, 'rb')as file:
        file_encoding = chardet.detect(file.read())['encoding']
    return file_encoding


def get_data(files: list):
    headers = ['Изготовитель ОС', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data = [headers]

    for file in files:
        with open(file, 'r', encoding=get_encoding(file)) as file:
            file_data = file.read()

        data_row = list()
        for line in file_data.split('\n'):
            for header in headers:
                row_item = re.findall(r'{}:\s+(.+)$'.format(header), line)
                if row_item:
                    data_row.append(row_item[0])

        main_data.append(data_row)

    return main_data


def write_csv(file, data_files):
    data = get_data(data_files)
    with open(file, 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            writer.writerow(row)


path = os.path.join(os.getcwd(), 'lesson_files')

files_txt = [os.path.join(path, file) for file in os.listdir(path) if re.findall(r'\.txt$', file)]
files_json = [os.path.join(path, file) for file in os.listdir(path) if re.findall(r'\.json$', file)]

# write_csv('my_file.csv', files_txt)


# 2.


def write_json(file, order_data):
    with open(file, 'r', encoding=get_encoding(file)) as json_file:
        data = json.load(json_file)

    data['orders'].append(order_data)
    with open(file, 'w', encoding=get_encoding(file)) as json_file:
        json.dump(data, json_file, indent=4)


my_order = {'item': 'iPhone 11', 'quantity': 1, 'price': 399, 'buyer': 'Mike', 'date': '10.07.2019'}
# write_json(files_json[0], my_order)


# 3.
currency_signs = {'DOLLAR_SIGN': '\u0024', 'LIRA_SIGN': '\u00A3', 'RUBLE_SIGN': '\u20BD', 'BITCOIN_SIGN': '\u20BF'}
data = {'list': [1, 2, 3], 'integer': 99, 'currency_signs': currency_signs}


with open('my_file.yaml', 'w') as yaml_file:
    yaml.safe_dump(data, yaml_file, default_flow_style=False, allow_unicode=True)

with open('my_file.yaml', 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

print(yaml_data)
