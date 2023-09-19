import logging
import os
import re


logger = logging.getLogger()
wdpath = os.getcwd()


values_extention = 'value.csv'
values_dir = 'values'


def read_data(file):
    with open(file, "r") as f:
        for i, line in enumerate(f):
            if 1 <= i <= 3:
                continue
            elif i == 4:
                headers_data = line[2:].split(',')
            elif i == 5:
                values_data = line.split(',')

    names = []
    unints = []
    descriptions = []

    for header in headers_data:
       names.append(re.split(r'\(.*?\)', header)[0].strip())
       descriptions.append(re.split(r'\(.*?\)', header)[1].strip())
       unints.append(re.findall(r'\(.*?\)', header)[0].strip())
    
    data = [names, values_data, unints, descriptions]

    return data


def write_new_values(data, path):
    """Вывод файла values.csv."""
    try:
        os.mkdir(values_dir)  # Создание папки "values", если ее нет
    except OSError:
        pass
    
    new_values_name = os.path.basename(path).replace(values_extention,'')
    new_path = wdpath + '\\' + values_dir + '\\' + new_values_name + '.csv'

    with open(new_path, 'w') as f:
        f.write("Name,Value,Target,Condition,Dimension,Description,Comments,\n")  # Создание файла "values.csv" с шапкой
        data_length = len(data[0])    


        for i in range(data_length):
            f.write(f'{data[0][i]},{data[1][i].strip()},,,{data[2][i]},{data[3][i]},\n')


def convert_values(values_paths):
    for path in values_paths:   
        data = read_data(path)
        [print(field) for field in data]
        write_new_values(data, path) 
    

def find_values_paths():
    """Поиск файлов c данными и обработка."""
    values_paths = []
    for root, dirs, files in os.walk(wdpath):
        for resf in files:
            if resf.endswith(values_extention) and root != 'values':
                values_paths.append(root + '\\' + os.path.basename(resf))
    #[print(path) for path in values_paths]
    return values_paths
