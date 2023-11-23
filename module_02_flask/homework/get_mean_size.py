import sys

data = sys.stdin.readlines()[1:]

def get_mean_size(data: list) -> None:
    total_size = 0
    count = 0
    if data:
        for line in data:
            if line[0] != 'd':
                columns = line.split()
                total_size += int(columns[4])
                count += 1
    else:
        print(f'В папке отсутствуют файлы')
        return None
    mean_size = total_size / count
    mean_size_format = "{:.2f}".format(mean_size)
    print(f'Общийй размер файлов в папке: {total_size} б')
    print(f'Средний размер файла в папке: {mean_size_format} б')


get_mean_size(data)
