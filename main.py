import logging
import os
import re


logger = logging.getLogger()
wdpath = os.getcwd()

curve_filename = 'curves'
curve_extention = 'curve.csv'
value_filename = 'values'
values_extention = 'value.csv'
values_paths = []
values_dir = 'values'


def configure_logging():
    logging.getLogger("matplotlib.font_manager").setLevel(level=logging.WARN)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('Python.log', 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():
    global res
    for root, dirs, files in os.walk(wdpath):
        for resf in files:
            # ищем curve.csv
            if resf.endswith(curve_extention):
                res = []
                curve_path = root + '\\' + os.path.basename(resf)
                process_file(curve_path)
                save_output_curve()
                res = []
            # ищем value.csv
            elif resf.endswith(values_extention) and root != 'values':
                values_paths.append(root + '\\' + os.path.basename(resf))
    convert_values(values_paths)


#Обработка файлов curve.csv
def process_file(curve_path):
    _iter = 1
    _res = []
    _res2 = []
    _res3 = []
    with open(curve_path, "r") as f:
        for line in f:
            if 1 <= _iter <= 3:
                _iter += 1
                continue
            elif _iter == 4:
                _num = line.find(' - ')
                _line = line[_num + 3:].strip()
                _res = _line.split()
                res.append(_res)
                _iter += 1
            elif _iter == 5:
                _line = line[2:].strip()
                _res = _line.split(',')
                for i in range(len(_res)):
                    _res[i] = _res[i].split()
                    _res2.append(_res[i][0])
                    _res3.append(_res[i][-1])
                res.append(_res2)
                res.append(_res3)
                _iter += 1
            else:
                res.append(line.strip().split(','))
                _iter += 1


#Запись файлов csv в папку curves
def save_output_curve():
    """Вывод файла curves.csv."""

    try:
        os.mkdir(curve_filename)  # Создание папки "curves", если ее нет
    except OSError:
        pass

    for i in range(len(res[0])):
        with open(f"{curve_filename}\\{res[0][i]}.csv", "w") as f:    # Запись файлов csv в папку curves
            for j in range(len(res)):
                if j == 0:
                    f.write(res[0][i] + "\n")
                else:
                    f.write(res[j][0] + ',' + res[j][i + 1] + "\n")


def read_data(file):
    with open(file, "r") as f:
        for i, line in enumerate(f):
            if 1 <= i <= 3:
                continue
            elif i == 4:
                headers_data = line[2:].split(',')
            elif i == 5:
                values_data = line.split(',')
                for j in range(len(values_data)):
                    values_data[j] = float(values_data[j])

    names = []
    unints = []
    descriptions = []

    for header in headers_data:
       names.append(re.split(r'\(.*?\)', header)[0].strip())
       descriptions.append(re.split(r'\(.*?\)', header)[1].strip())
       unints.append(re.findall(r'\(.*?\)', header)[0].strip())

    i = 0
    for unint in unints:
        if unint == '(degC)':
            values_data[i] = "{:.0f}".format(values_data[i])
        i += 1

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



configure_logging()
main()
logger.info("ALL DONE")