import logging
import os


logger = logging.getLogger()
wdpath = os.getcwd()

curve_filename = 'curves'
curve_extention = 'curve.csv'
value_filename = 'values'
value_extention = '.value.csv'


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
            elif resf.endswith(value_extention):
                den4ic = "сучка"


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


configure_logging()
main()
logger.info("ALL DONE")