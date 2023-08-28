import os
import re
import logging
import shutil

logger = logging.getLogger()

wdpath = os.getcwd()

input_name = 'curve_Comsol.csv'
output_dir = 'curves'
output_name = 'curves.csv'

values_dir = 'values'
points_name = 'values.csv'
pics_dir = 'pictures'
picture_name = 'Mesh convergence'

# Для обработки файла параметров
csvpath = wdpath + '\\' + input_name
pattern = r"(P\d{1,3})\s-\s([a-zA-Z _.@0-9]+)\s?(\[.+?\])*"
pattern_2 = r"DP\s.*"
res = []


def configure_logging():
    logging.getLogger("matplotlib.font_manager").setLevel(level=logging.WARN)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('python.log', 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def process_file(csvpath):
    """Обработка файла export.csv
    (в нем содержатся параметы WB)."""
    _iter = 1
    _res = []
    with open(csvpath, "r") as f:
        for line in f:
            if 1 <= _iter <= 3:
                _iter += 1
                continue
            elif _iter == 4:
                _num = line.find(' - ')
                res.append(line[_num + 3:].strip())
                _iter += 1
            elif _iter == 5:
                _line = line[2:].strip()
                _res = _line.split(',')
                _res = _res[:2]
                _res[0] = _res[0].split()
                _res[1] = _res[1].split()
                res.append(str(_res[0][0]) + ',' + str(_res[1][0]))
                res.append(str(_res[0][1]) + ',' + str(_res[1][1]))
                _iter += 1
            else:
                res.append(line.strip().split(','))
                _iter += 1


def save_output():
    """Вывод файла values.csv."""

    try:
        os.mkdir(values_dir)  # Создание папки "values", если ее нет
    except OSError:
        pass

    with open(f"{values_dir}\\{points_name}", "w") as f:
        f.write("Name,Value,Target,Condition,Dimension,Description,Comments,\n")  # Создание файла "values.csv" с шапкой
        for e in res:
            if '[' in e[2]:
                dim = (e[2].split('[')[-1]).split(']')[0]
            else:
                dim = ''

            a = f'{e[1].strip()},{e[3]} ,,, {dim} ,,,\n'
            f.write(a)


def save_output_comsol():
    """Вывод файла curves.csv."""

    try:
        os.mkdir(output_dir)  # Создание папки "curves", если ее нет
    except OSError:
        pass

    with open(f"{output_dir}\\{output_name}", "w") as f:    # Создание файла "curves.csv"
        for _iter in range(len(res)):
            if 0 <= _iter <= 2:
                f.write(res[_iter] + "\n")
            else:
                f.write(res[_iter][0] + ',' + res[_iter][1] + "\n")


def copypic():
    """Копирование изображений."""

    if not os.path.exists(pics_dir):  # Создание папки "pictures", если ее нет
        os.makedirs(pics_dir)
        logger.info('Dir pictures created')

    for root, dirs, files in os.walk(wdpath):  # Обход по всем папкам
        for pic in files:
            if pic.endswith('.descr') or pic.endswith('.png'):
                pic_name = os.path.basename(pic)  # Возврат названия файла
                try:
                    shutil.copy2(root + '\\' + pic_name, os.getcwd() + '\\' + pics_dir)  # Копирование файлов

                except BaseException:
                    logger.error(f'copypic error')
                    pass


configure_logging()

process_file(csvpath)
save_output_comsol()

#copypic()

logger.info("ALL DONE")
